from unittest import TestCase
import unittest.mock
from molecupy.structures import ResiduicStructure, Residue, AtomicStructure
from molecupy import NoResiduesError

class ResiduicStructureTest(TestCase):

    def setUp(self):
        self.residues = [unittest.mock.Mock(spec=Residue) for _ in range(10)]



class ResiduicStructureCreationTests(ResiduicStructureTest):

    def test_can_create_residuic_structure(self):
        residuic_structure = ResiduicStructure(*self.residues)
        self.assertIsInstance(residuic_structure, AtomicStructure)
        self.assertEqual(residuic_structure._residues, set(self.residues))


    def test_can_only_create_residuic_structure_with_residues(self):
        with self.assertRaises(TypeError):
            ResiduicStructure("Atom1", "Atom2")


    def test_cannot_make_empty_atomic_structure(self):
        with self.assertRaises(NoResiduesError):
            ResiduicStructure()


    def test_residuic_structure_repr(self):
        residuic_structure = ResiduicStructure(*self.residues)
        self.assertEqual(str(residuic_structure), "<ResiduicStructure (10 residues)>")



class ResiduicStructurePropertyTests(ResiduicStructureTest):

    def test_can_get_residues(self):
        residuic_structure = ResiduicStructure(*self.residues)
        self.assertEqual(residuic_structure.residues(), set(self.residues))


    def test_residuic_structure_residues_is_read_only(self):
        residue11 = unittest.mock.Mock(spec=Residue)
        residuic_structure = ResiduicStructure(*self.residues)
        self.assertEqual(len(residuic_structure.residues()), 10)
        residuic_structure.residues().add(residue11)
        self.assertEqual(len(residuic_structure.residues()), 10)


    def test_can_exclude_missing_residues(self):
        for residue in self.residues:
            residue.is_missing.return_value = False
        self.residues[6].is_missing.return_value = True
        residuic_structure = ResiduicStructure(*self.residues)
        self.assertEqual(
         len(residuic_structure.residues(include_missing=False)),
         9
        )
        self.assertNotIn(
         self.residues[6],
         residuic_structure.residues(include_missing=False)
        )
