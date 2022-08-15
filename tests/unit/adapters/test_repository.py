import pytest

from compenv.adapters.entity import DJComputationRecord
from compenv.adapters.repository import DJRepository
from compenv.model.computation import ComputationRecord, Identifier
from compenv.model.record import Record
from compenv.types import PrimaryKey

from ..conftest import FakeTranslator
from .conftest import FakeRecordTableFacade


@pytest.fixture
def repo(fake_translator: FakeTranslator, fake_facade: FakeRecordTableFacade) -> DJRepository:
    return DJRepository(fake_translator, fake_facade)


@pytest.fixture
def comp_rec(identifier: Identifier, record: Record) -> ComputationRecord:
    return ComputationRecord(identifier, record)


@pytest.fixture
def add_computation_record(repo: DJRepository, comp_rec: ComputationRecord) -> None:
    repo.add(comp_rec)


@pytest.mark.usefixtures("add_computation_record")
class TestAdd:
    @staticmethod
    def test_raises_error_if_already_existing(repo: DJRepository, comp_rec: ComputationRecord) -> None:
        with pytest.raises(ValueError, match="already exists!"):
            repo.add(comp_rec)

    @staticmethod
    def test_inserts_dj_computation_record(
        fake_facade: FakeRecordTableFacade, primary: PrimaryKey, dj_comp_rec: DJComputationRecord
    ) -> None:
        assert fake_facade.get(primary) == dj_comp_rec


def test_raises_error_if_not_existing(repo: DJRepository, identifier: Identifier) -> None:
    with pytest.raises(KeyError, match="does not exist!"):
        _ = repo.get(identifier)


class TestGet:
    @staticmethod
    @pytest.mark.usefixtures("add_computation_record")
    def test_gets_computation_record_if_existing(
        repo: DJRepository, comp_rec: ComputationRecord, identifier: Identifier
    ) -> None:
        assert repo.get(identifier) == comp_rec


def test_iteration(repo: DJRepository, comp_rec: ComputationRecord) -> None:
    repo.add(comp_rec)
    assert list(iter(repo)) == [comp_rec.identifier]


def test_length(repo: DJRepository, comp_rec: ComputationRecord) -> None:
    repo.add(comp_rec)
    assert len(repo) == 1


def test_repr(repo: DJRepository) -> None:
    assert repr(repo) == "DJRepository(translator=FakeTranslator(), facade=FakeRecordTableFacade())"
