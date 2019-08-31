import logging
from abc import abstractmethod
from contextlib import contextmanager
from typing import Any, Type, Union
from flask import g, has_request_context
from sqlalchemy import create_engine, Column
from sqlalchemy.sql.elements import ClauseElement
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from werkzeug.exceptions import NotFound

_Base = declarative_base()


class Base(_Base):
    __abstract__ = True

    @classmethod
    def _build_query(
        cls, session: Session, query_target, where_clause=None, order_by=None
    ):
        query = session.query(query_target)

        if where_clause is not None:
            query = query.filter(where_clause)

        if order_by is not None:
            query = query.order_by(order_by)

        return query

    @classmethod
    def get_all(
        cls,
        *,
        read_session: Session,
        where_clause: Union[ClauseElement, bool] = None,
        order_by: ClauseElement = None,
    ):
        """
        전달된 인자들을 통해 쿼리를 생성하고, .all()의 결과를 반환합니다.
        :param read_session: SQLAlchemy session
        :param where_clause: 적용할 where clause
        :param order_by: 적용할 order by clause
        """
        query = cls._build_query(
            read_session, cls, where_clause=where_clause, order_by=order_by
        )

        return query.all()

    @classmethod
    def get_first(
        cls,
        *,
        read_session: Session,
        where_clause: Union[ClauseElement, bool] = True,
        order_by: ClauseElement = None,
    ):
        """
        전달된 인자들을 통해 쿼리를 생성하고, None 여부에 상관없이 .first()의 결과를 리턴합니다.
        :param read_session: SQLAlchemy session
        :param where_clause: 적용할 where clause
        :param order_by: 적용할 order by clause
        """
        query = cls._build_query(
            read_session, cls, where_clause=where_clause, order_by=order_by
        )

        return query.first()

    @classmethod
    def get_one(
        cls,
        *,
        read_session: Session,
        where_clause: Union[ClauseElement, bool] = True,
        order_by: ClauseElement = None,
        exception_cls: Type[Exception] = NotFound,
        message: str = None,
    ):
        """
        1. 전달된 인자들을 통해 쿼리를 생성하고
        2. .first() 후 결과가 None이면 인자 정보들을 통해 exception raise,
        3. None이 아니라면 해당 객체를 리턴
        :param read_session: SQLAlchemy session
        :param where_clause: 적용할 where clause
        :param order_by: 적용할 order by clause
        :param exception_cls: .first()의 결과가 None인 경우 raise할 exception
        :param message: .first()의 결과가 None인 경우 abort할 때 사용할 메시지
        """
        res = cls.get_first(
            read_session=read_session, where_clause=where_clause, order_by=order_by
        )

        if res is None:
            raise exception_cls(message)
        else:
            return res

    @classmethod
    def get_scalar(
        cls,
        *,
        read_session: Session,
        column: Column,
        where_clause: Union[ClauseElement, bool] = True,
        order_by: ClauseElement = None,
    ) -> Any:
        """
        전달된 인자들을 통해 쿼리를 생성하고, column에 해당하는 데이터를 반환합니다.
        :param read_session: SQLAlchemy session
        :param column: 반환받고자 하는 컬럼
        :param where_clause: 적용할 where clause
        :param order_by: 적용할 order by clause
        """
        query = cls._build_query(read_session, column, where_clause, order_by)

        return query.scalar()


class DB:
    @abstractmethod
    def extract_create_engine_kwargs(self, flask_app) -> dict:
        """
        `self.checkout_new_session`을 초기화하기 위해 호출하는
        `sqlalchemy.create_app` 함수에 전달할 인자들을 dictionary로 반환합니다.
        """

        pass

    @property
    @abstractmethod
    def attribute_name_on_g(self) -> str:
        """
        g 객체에 session 객체를 저장할 때 사용할 attribute name입니다.
        setattr(obj, name, value)에서 `name` 자리에 사용됩니다.
        """

        pass

    @property
    def session(self) -> Session:
        """
        g 객체에서 session 객체를 가져와 반환합니다.
        현재 context에 대해 checkout된 session이 없으며 request context가 활성화되어 있는 경우, 새로 생성합니다.
        """

        session = getattr(g, self.attribute_name_on_g, None)

        if session is None and has_request_context():
            session = self.checkout_new_session()
            setattr(g, self.attribute_name_on_g, session)

        return session

    @session.setter
    def session(self, value: Session):
        """
        g 객체에 session 객체를 저장합니다.
        """

        setattr(g, self.attribute_name_on_g, value)

    @contextmanager
    def session_context(self):
        session = self.checkout_new_session()
        yield session
        session.close()

    def __init__(self, flask_app=None):
        self.engine = None
        self.checkout_new_session = None

        if flask_app is not None:
            self.init_app(flask_app)

    def init_app(self, flask_app):
        self.engine = create_engine(**self.extract_create_engine_kwargs(flask_app))
        self.checkout_new_session = sessionmaker(self.engine)

        @flask_app.teardown_appcontext
        def teardown_appcontext(_):
            """
            context에 대해 session이 한 번 이상 checkout되었다면 이를 close해주기 위한 teardown callback
            """

            session = self.session

            if session is not None:
                session.close()

    def check_db_status(self):
        try:
            self._check_db_connection()
            return True
        except Exception as e:
            logging.error("DB connection is failed with : {}".format(e))
            return False

    def _check_db_connection(self):
        """Check DB Status"""
        connection = self.engine.connect()
        connection.close()


class WriteDB(DB):
    def extract_create_engine_kwargs(self, flask_app):
        return {"name_or_url": flask_app.config["WRITE_DB_URL"]}

    attribute_name_on_g = "write_db_session"


# class ReadDB(DB):
#     def extract_create_engine_kwargs(self, flask_app):
#         return {"name_or_url": flask_app.config["READ_DB_URL"]}
#
#     attribute_name_on_g = "read_db_session"
#
#
# class BatchDB(DB):
#     def extract_create_engine_kwargs(self, flask_app):
#         return {"name_or_url": flask_app.config["BATCH_DB_URL"]}
#
#     attribute_name_on_g = "batch_db_session"
