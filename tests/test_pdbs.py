from unittest import TestCase
import unittest.mock
from molecupy.pdb import Pdb
from molecupy.pdbdatafile import PdbDataFile
from molecupy.structures import Model, SmallMolecule, Chain, Residue

class PdbTest(TestCase):

    def setUp(self):
        self.data_file = unittest.mock.Mock(spec=PdbDataFile)
        self.data_file.models.return_value = [
         {"model_id": 1, "start_record": 0, "end_record": 0}
        ]
        self.data_file.heteroatoms.return_value = []
        self.data_file.atoms.return_value = []


class PdbCreationTests(PdbTest):

    def test_can_create_pdb(self):
        pdb = Pdb(self.data_file)
        self.assertIs(pdb.data_file(), self.data_file)


    def test_can_get_data_attributes(self):
        self.data_file.classification.return_value = "val1",
        self.data_file.deposition_date.return_value = "val2",
        self.data_file.pdb_code.return_value = "val3",
        self.data_file.is_obsolete.return_value = "val4",
        self.data_file.obsolete_date.return_value = "val5",
        self.data_file.replacement_code.return_value = "val6",
        self.data_file.title.return_value = "val7",
        self.data_file.split_codes.return_value = "val8",
        self.data_file.caveat.return_value = "val9",
        self.data_file.keywords.return_value = "val10",
        self.data_file.experimental_techniques.return_value = "val11",
        self.data_file.model_count.return_value = "val12",
        self.data_file.model_annotations.return_value = "val13",
        self.data_file.authors.return_value = "val14",
        self.data_file.revisions.return_value = "val15",
        self.data_file.supercedes.return_value = "val16",
        self.data_file.supercede_date.return_value = "val17",
        self.data_file.journal.return_value = "val18"
        pdb = Pdb(self.data_file)
        self.assertIs(
         pdb.classification(),
         self.data_file.classification()
        )
        self.assertIs(
         pdb.deposition_date(),
         self.data_file.deposition_date()
        )
        self.assertIs(
         pdb.pdb_code(),
         self.data_file.pdb_code(),
        )
        self.assertIs(
         pdb.is_obsolete(),
         self.data_file.is_obsolete()
        )
        self.assertIs(
         pdb.obsolete_date(),
         self.data_file.obsolete_date()
        )
        self.assertIs(
         pdb.replacement_code(),
         self.data_file.replacement_code()
        )
        self.assertIs(
         pdb.title(),
         self.data_file.title()
        )
        self.assertIs(
         pdb.split_codes(),
         self.data_file.split_codes()
        )
        self.assertIs(
         pdb.caveat(),
         self.data_file.caveat()
        )
        self.assertIs(
         pdb.keywords(),
         self.data_file.keywords()
        )
        self.assertIs(
         pdb.experimental_techniques(),
         self.data_file.experimental_techniques()
        )
        self.assertIs(
         pdb.model_count(),
         self.data_file.model_count()
        )
        self.assertIs(
         pdb.model_annotations(),
         self.data_file.model_annotations()
        )
        self.assertIs(
         pdb.revisions(),
         self.data_file.revisions()
        )
        self.assertIs(
         pdb.supercedes(),
         self.data_file.supercedes()
        )
        self.assertIs(
         pdb.supercede_date(),
         self.data_file.supercede_date()
        )
        self.assertIs(
         pdb.journal(),
         self.data_file.journal()
        )


    def test_pdb_repr(self):
        pdb = Pdb(self.data_file)
        self.data_file.pdb_code.return_value = None
        self.assertEqual(str(pdb), "<Pdb (????)>")
        self.data_file.pdb_code.return_value = "1SAM"
        self.assertEqual(str(pdb), "<Pdb (1SAM)>")



class PdbModelsTests(PdbTest):

    def test_single_model(self):
        pdb = Pdb(self.data_file)
        self.assertEqual(len(pdb.models()), 1)
        self.assertIsInstance(pdb.models()[0], Model)


    def test_multiple_models(self):
        self.data_file.models.return_value = [
         {"model_id": 1, "start_record": 1, "end_record": 3},
         {"model_id": 2, "start_record": 4, "end_record": 6}
        ]
        pdb = Pdb(self.data_file)
        self.assertEqual(len(pdb.models()), 2)
        self.assertIsInstance(pdb.models()[0], Model)
        self.assertIsInstance(pdb.models()[1], Model)


    def test_one_model_access(self):
        self.data_file.models.return_value = [
         {"model_id": 1, "start_record": 1, "end_record": 3},
         {"model_id": 2, "start_record": 4, "end_record": 6}
        ]
        pdb = Pdb(self.data_file)
        self.assertIs(pdb.models()[0], pdb.model())



class PdbSmallMoleculeTests(PdbTest):

    def test_single_small_molecule(self):
        self.data_file.heteroatoms.return_value = [
         {
          "atom_id": 8237,
          "atom_name": "CA",
          "alt_loc": None,
          "residue_name": "123",
          "chain_id": "A",
          "residue_id": 1001,
          "insert_code": "",
          "x": 13.872,
          "y": -2.555,
          "z": -29.045,
          "occupancy": 1.0,
          "temperature_factor": 27.36,
          "element": "C",
          "charge": None,
          "model_id": 1
         }, {
          "atom_id": 8238,
          "atom_name": "MG",
          "alt_loc": None,
          "residue_name": "123",
          "chain_id": "A",
          "residue_id": 1001,
          "insert_code": "",
          "x": 13.872,
          "y": -2.555,
          "z": -29.045,
          "occupancy": 1.0,
          "temperature_factor": 27.36,
          "element": "MG",
          "charge": None,
          "model_id": 1
         }
        ]
        pdb = Pdb(self.data_file)
        self.assertEqual(len(pdb.model().small_molecules()), 1)
        self.assertIsInstance(list(pdb.model().small_molecules())[0], SmallMolecule)
        self.assertEqual(len(list(pdb.model().small_molecules())[0].atoms()), 2)


    def test_multiple_small_molecules(self):
        self.data_file.heteroatoms.return_value = [
         {
          "atom_id": 8237,
          "atom_name": "CA",
          "alt_loc": None,
          "residue_name": "123",
          "chain_id": "A",
          "residue_id": 1001,
          "insert_code": "A",
          "x": 13.872,
          "y": -2.555,
          "z": -29.045,
          "occupancy": 1.0,
          "temperature_factor": 27.36,
          "element": "C",
          "charge": None,
          "model_id": 1
         }, {
          "atom_id": 8238,
          "atom_name": "MG",
          "alt_loc": None,
          "residue_name": "123",
          "chain_id": "A",
          "residue_id": 1001,
          "insert_code": "A",
          "x": 13.872,
          "y": -2.555,
          "z": -29.045,
          "occupancy": 1.0,
          "temperature_factor": 27.36,
          "element": "MG",
          "charge": None,
          "model_id": 1
         }, {
          "atom_id": 8239,
          "atom_name": "CA",
          "alt_loc": None,
          "residue_name": "MOL",
          "chain_id": "A",
          "residue_id": 1002,
          "insert_code": "",
          "x": 13.872,
          "y": -2.555,
          "z": -29.045,
          "occupancy": 1.0,
          "temperature_factor": 27.36,
          "element": "C",
          "charge": None,
          "model_id": 1
         }, {
          "atom_id": 8240,
          "atom_name": "MG",
          "alt_loc": None,
          "residue_name": "MOL",
          "chain_id": "A",
          "residue_id": 1002,
          "insert_code": "",
          "x": 13.872,
          "y": -2.555,
          "z": -29.045,
          "occupancy": 1.0,
          "temperature_factor": 27.36,
          "element": "MG",
          "charge": None,
          "model_id": 1
         }
        ]
        pdb = Pdb(self.data_file)
        self.assertEqual(len(pdb.model().small_molecules()), 2)
        self.assertEqual(
         set([mol.molecule_name() for mol in pdb.model().small_molecules()]),
         set(["123", "MOL"])
        )
        self.assertEqual(
         set([mol.molecule_id() for mol in pdb.model().small_molecules()]),
         set(["A1002", "A1001A"])
        )


    def test_single_small_molecules_in_multiple_models(self):
        self.data_file.models.return_value = [
         {"model_id": 1, "start_record": 0, "end_record": 1},
         {"model_id": 2, "start_record": 2, "end_record": 3}
        ]
        self.data_file.heteroatoms.return_value = [
         {
          "atom_id": 8237,
          "atom_name": "CA",
          "alt_loc": None,
          "residue_name": "123",
          "chain_id": "A",
          "residue_id": 1001,
          "insert_code": "",
          "x": 13.872,
          "y": -2.555,
          "z": -29.045,
          "occupancy": 1.0,
          "temperature_factor": 27.36,
          "element": "C",
          "charge": None,
          "model_id": 1
         }, {
          "atom_id": 8238,
          "atom_name": "MG",
          "alt_loc": None,
          "residue_name": "123",
          "chain_id": "A",
          "residue_id": 1001,
          "insert_code": "",
          "x": 13.872,
          "y": -2.555,
          "z": -29.045,
          "occupancy": 1.0,
          "temperature_factor": 27.36,
          "element": "MG",
          "charge": None,
          "model_id": 1
         }, {
          "atom_id": 8237,
          "atom_name": "CA",
          "alt_loc": None,
          "residue_name": "123",
          "chain_id": "A",
          "residue_id": 1001,
          "insert_code": "",
          "x": 13.872,
          "y": -2.555,
          "z": -29.045,
          "occupancy": 1.0,
          "temperature_factor": 27.36,
          "element": "C",
          "charge": None,
          "model_id": 2
         }, {
          "atom_id": 8238,
          "atom_name": "MG",
          "alt_loc": None,
          "residue_name": "123",
          "chain_id": "A",
          "residue_id": 1001,
          "insert_code": "",
          "x": 13.872,
          "y": -2.555,
          "z": -29.045,
          "occupancy": 1.0,
          "temperature_factor": 27.36,
          "element": "MG",
          "charge": None,
          "model_id": 2
         }
        ]
        pdb = Pdb(self.data_file)
        self.assertEqual(len(pdb.models()[0].small_molecules()), 1)
        self.assertEqual(len(pdb.models()[1].small_molecules()), 1)
        self.assertIsNot(
         [pdb.models()[0].small_molecules()][0],
         [pdb.models()[1].small_molecules()][0]
        )



class PdbChainTests(PdbTest):

    def setUp(self):
        PdbTest.setUp(self)
        self.data_file.atoms.return_value = [
         {
          "atom_id": 107,
          "atom_name": "N",
          "alt_loc": None,
          "residue_name": "GLY",
          "chain_id": "A",
          "residue_id": 13,
          "insert_code": "",
          "x": 12.681,
          "y": 37.302,
          "z": -25.211,
          "occupancy": 1.0,
          "temperature_factor": 15.56,
          "element": "N",
          "charge": None,
          "model_id": 1
         }, {
          "atom_id": 108,
          "atom_name": "CA",
          "alt_loc": None,
          "residue_name": "GLY",
          "chain_id": "A",
          "residue_id": 13,
          "insert_code": "",
          "x": 11.982,
          "y": 37.996,
          "z": -26.241,
          "occupancy": 1.0,
          "temperature_factor": 16.92,
          "element": "C",
          "charge": None,
          "model_id": 1
         }, {
          "atom_id": 109,
          "atom_name": "N",
          "alt_loc": None,
          "residue_name": "MET",
          "chain_id": "A",
          "residue_id": 13,
          "insert_code": "A",
          "x": 12.681,
          "y": 37.302,
          "z": -25.211,
          "occupancy": 1.0,
          "temperature_factor": 15.56,
          "element": "N",
          "charge": None,
          "model_id": 1
         }, {
          "atom_id": 110,
          "atom_name": "CA",
          "alt_loc": None,
          "residue_name": "MET",
          "chain_id": "A",
          "residue_id": 13,
          "insert_code": "A",
          "x": 11.982,
          "y": 37.996,
          "z": -26.241,
          "occupancy": 1.0,
          "temperature_factor": 16.92,
          "element": "C",
          "charge": None,
          "model_id": 1
         }
        ]


    def test_single_chain(self):
        pdb = Pdb(self.data_file)
        self.assertEqual(len(pdb.model().chains()), 1)
        chain = list(pdb.model().chains())[0]
        self.assertIsInstance(chain, Chain)
        self.assertEqual(chain.chain_id(), "A")
        self.assertEqual(len(chain.residues()), 2)
        self.assertIsInstance(chain.residues()[0], Residue)
        self.assertEqual(chain.residues()[0].residue_id(), "A13")
        self.assertEqual(chain.residues()[0].residue_name(), "GLY")
        self.assertEqual(chain.residues()[1].residue_id(), "A13A")
        self.assertEqual(chain.residues()[1].residue_name(), "MET")


    def test_multiple_chains(self):
        atoms = self.data_file.atoms()
        atoms[2]["chain_id"] = atoms[3]["chain_id"] = "B"
        self.data_file.atoms.return_value = atoms
        pdb = Pdb(self.data_file)
        self.assertEqual(len(pdb.model().chains()), 2)
        self.assertEqual(
         set([chain.chain_id() for chain in pdb.model().chains()]),
         set(["A", "B"])
        )
        self.assertEqual(
         set([len(chain.residues()) for chain in pdb.model().chains()]),
         set([1, 1])
        )


    def test_multiple_models(self):
        self.data_file.models.return_value = [
         {"model_id": 1, "start_record": 0, "end_record": 1},
         {"model_id": 2, "start_record": 2, "end_record": 3}
        ]
        atoms = self.data_file.atoms()
        atoms[2]["model_id"] = atoms[3]["model_id"] = 2
        self.data_file.atoms.return_value = atoms
        pdb = Pdb(self.data_file)
        self.assertEqual(len(pdb.models()[0].chains()), 1)
        self.assertEqual(len(pdb.models()[1].chains()), 1)
        self.assertIsNot(
         [pdb.models()[0].chains()][0],
         [pdb.models()[1].chains()][0]
        )
