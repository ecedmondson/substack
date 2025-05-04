
import logging
import time
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Generator, Optional

from sqlalchemy import create_engine, exc, text
from sqlalchemy.orm import Session

from settings.connection_settings import DBConnectionSettings

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

# Uncomment the following to log SQL queries
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class DatabaseEngineError(Exception):
    pass


class Connection:
    def __init__(
        self,
        pool_size: int = 5,
        max_overflow: int = 10,
        wait_for_server_time: timedelta = timedelta(minutes=2),
        retry_time: timedelta = timedelta(seconds=10),
    ):
        self.wait_for_server_time = wait_for_server_time
        self.retry_time = retry_time
        self.engine = create_engine(
            DBConnectionSettings().url,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
    
    def wait_for_connection(self):
        try:
            self.attempt_connection()
        except Exception:
            self.engine.dispose()
            raise DatabaseEngineError(
                f"Unable to connect to database {connection_settings.url} "
                f"after {self.wait_for_server_time.seconds} seconds"
            )

    def attempt_connection(
        self,
    ) -> None:
        start_time = datetime.now()
        connection_exception = self.connection_alive()
        if connection_exception is None:
            return
        next_poll = start_time + self.retry_time
        timeout_time = start_time + self.wait_for_server_time
        while next_poll < timeout_time:
            logger.warning(
                "Waiting for server. Next retry at %s will timeout at %s.",
                next_poll,
                timeout_time,
            )
            sleep_time = (next_poll - datetime.now()).total_seconds()
            if sleep_time > 0:
                time.sleep(sleep_time)
            connection_exception = self.connection_alive()
            if connection_exception is None:
                break
            next_poll += self.retry_time
        else:
            raise connection_exception
        logger.info(
            "Connection now available after %s seconds",
            (datetime.now() - start_time).total_seconds(),
        )

    def connection_alive(self) -> Optional[Exception]:
        try:
            with Session(self.engine) as session:
                logger.debug("Trying to connect to database...")
                session.query(text("1")).from_statement(text("SELECT 1")).all()  # type: ignore

            logger.debug("Connection alive!")
            return None
        except (exc.OperationalError, exc.ProgrammingError, RuntimeError) as ex:
            logger.warning("Connection to server failed: %s", str(ex))
            return ex

connection = Connection()

def get_db():
    session = Session(connection.engine)
    try:
        yield session
    finally:
        session.close()