from datetime import date
import re
import atomium
from unittest import TestCase

class DataDictTest(TestCase):

    def open(self, name):
        return {e: atomium.open(
         f"tests/integration/files/{name}.{e}", data_dict=True
        ) for e in ("cif", "mmtf", "pdb")}
    

    def check(self, dicts, subdict, values):
        for ext, d in dicts.items():
            d = d[subdict]
            for key, value in values.items():
                # Is this key specific to one filetype that isn't this one?
                if re.search("_(cif|mmtf|pdb)$", key) and key.split("_")[-1] != ext:
                    continue
                # Is there a more specific version of this key?
                if any(k == f"{key}_{ext}" for k in values.keys()):
                    continue
                try:
                    self.assertEqual(d[key.replace(f"_{ext}", "")], value)
                except AssertionError as e:
                    raise AssertionError(f"({ext.upper()}) {str(e)}")



class DescriptionDictTests(DataDictTest):

    def test_1lol_data_dict_description(self):
        data_dicts = self.open("1lol")
        self.check(data_dicts, "description", {
         "code": "1LOL",
         "title": "Crystal structure of orotidine monophosphate decarboxylase complex with XMP",
         "title_pdb": "CRYSTAL STRUCTURE OF OROTIDINE MONOPHOSPHATE DECARBOXYLASE COMPLEX WITH XMP",
         "deposition_date": date(2002, 5, 6),
         "classification": "LYASE", "classification_mmtf": None,
         "keywords_cif": ["TIM barrel", "LYASE"],
         "keywords_mmtf": [],
         "keywords_pdb": ["TIM BARREL", "LYASE"],
         "authors_cif": ["Wu, N.", "Pai, E.F."],
         "authors_mmtf": [],
         "authors_pdb": ["N.WU", "E.F.PAI"]
        })



class ExperimentDictTests(DataDictTest):

    def test_1lol_data_dict_experiment(self):
        data_dicts = self.open("1lol")
        missing_residues = [{"id": id, "name": name} for id, name in zip([
         "A.1", "A.2", "A.3", "A.4", "A.5", "A.6", "A.7", "A.8", "A.9", "A.10",
         "A.182", "A.183", "A.184", "A.185", "A.186", "A.187", "A.188", "A.189",
         "A.223", "A.224", "A.225", "A.226", "A.227", "A.228", "A.229", "B.1001",
         "B.1002", "B.1003", "B.1004", "B.1005", "B.1006", "B.1007", "B.1008",
         "B.1009", "B.1010", "B.1182", "B.1183", "B.1184", "B.1185", "B.1186"
        ], [
         "LEU", "ARG", "SER", "ARG", "ARG", "VAL", "ASP", "VAL", "MET", "ASP",
         "VAL", "GLY", "ALA", "GLN", "GLY", "GLY", "ASP", "PRO", "LYS", "ASP",
         "LEU", "LEU", "ILE", "PRO", "GLU", "LEU", "ARG", "SER", "ARG", "ARG",
         "VAL", "ASP", "VAL", "MET", "ASP", "VAL", "GLY", "ALA", "GLN", "GLY"
        ])]
        self.check(data_dicts, "experiment", {
         "technique": "X-RAY DIFFRACTION",
         "source_organism_cif": "Methanothermobacter thermautotrophicus str. Delta H",
         "source_organism_mmtf": None,
         "source_organism_pdb": "METHANOTHERMOBACTER THERMAUTOTROPHICUS STR. DELTA H",
         "expression_system_cif": "Escherichia coli",
         "expression_system_mmtf": None,
         "expression_system_pdb": "ESCHERICHIA COLI",
         "missing_residues": missing_residues, "missing_residues_mmtf": []
        })
        

    def test_1cbn_data_dict_experiment(self):
        data_dicts = self.open("1cbn")
        self.check(data_dicts, "experiment", {
         "technique": "X-RAY DIFFRACTION",
         "source_organism_cif": "Crambe hispanica subsp. abyssinica",
         "source_organism_mmtf": None,
         "source_organism_pdb": "CRAMBE HISPANICA SUBSP. ABYSSINICA",
         "expression_system": None,
        })



class QualityDictTests(DataDictTest):

    def test_1lol_data_dict_quality(self):
        data_dicts = self.open("1lol")
        self.check(data_dicts, "quality", {
         "resolution": 1.9, "rvalue": 0.193, "rfree": 0.229
        })
    

    def test_5xme_data_dict_quality(self):
        data_dicts = self.open("5xme")
        self.check(data_dicts, "quality", {
         "resolution": None, "rvalue": None, "rfree": None
        })



class GeometryDictTests(DataDictTest):

    def test_1lol_data_dict_geometry(self):
        data_dicts = self.open("1lol")
        self.check(data_dicts, "geometry", {
         "crystallography": {"space_group": "P 1 21 1", "unit_cell": [
          57.57, 55.482, 66.129, 90, 94.28, 90
         ]},
         "assemblies_cif": [{
          "id": 1, "software": "PISA", "delta_energy": -31.0,
          "buried_surface_area": 5230, "surface_area": 16550,
          "transformations": [{
           "chains": ["A", "B", "C", "D", "E", "F", "G", "H"],
           "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
           "vector": [0.0, 0.0, 0.0]
          }]
         }],
         "assemblies_mmtf": [{
          "id": 1, "software": None, "delta_energy": None,
          "buried_surface_area": None, "surface_area": None,
          "transformations": [{
           "chains": ["A", "B", "C", "D", "E", "F", "G", "H"],
           "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
           "vector": [0.0, 0.0, 0.0]
          }]
         }],
         "assemblies_pdb": [{
          "id": 1, "software": "PISA", "delta_energy": -31.0,
          "buried_surface_area": 5230, "surface_area": 16550,
          "transformations": [{
           "chains": ["A", "B"],
           "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
           "vector": [0.0, 0.0, 0.0]
          }]
         }]
        })


    def test_5xme_data_dict_geometry(self):
        data_dicts = self.open("5xme")
        self.check(data_dicts, "geometry", {
         "crystallography": {},
         "crystallography_pdb": {
          "space_group": "P 1", "unit_cell": [1, 1, 1, 90, 90, 90]
         }
        })

        
    def test_1xda_data_dict_geometry(self):
        # Multiple assemblies with different chains
        data_dicts = self.open("1xda")
        for d in data_dicts.values():
            self.assertEqual(len(d["geometry"]["assemblies"]), 12)
        self.assertEqual(data_dicts["cif"]["geometry"]["assemblies"][0], {
         "id": 1, "software": "PISA", "delta_energy": -7,
         "buried_surface_area": 1720, "surface_area": 3980,
         "transformations": [{
          "chains": ["A", "B", "I", "J", "K", "L", "Y", "Z"],
          "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 0.0, 0.0]
         }]
        })
        self.assertEqual(data_dicts["mmtf"]["geometry"]["assemblies"][0], {
         "id": 1, "software": None, "delta_energy": None,
         "buried_surface_area": None, "surface_area": None,
         "transformations": [{
          "chains": ["A", "B", "I", "J", "K", "L", "Y", "Z"],
          "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 0.0, 0.0]
         }]
        })
        self.assertEqual(data_dicts["pdb"]["geometry"]["assemblies"][0], {
         "id": 1, "software": "PISA", "delta_energy": -7,
         "buried_surface_area": 1720, "surface_area": 3980,
         "transformations": [{
          "chains": ["A", "B"],
          "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 0.0, 0.0]
         }]
        })
        self.assertEqual(data_dicts["cif"]["geometry"]["assemblies"][4], {
         "id": 5, "software": "PISA", "delta_energy": -332.0,
         "buried_surface_area": 21680.0, "surface_area": 12240.0,
         "transformations": [{
          "chains": ["E", "F", "G", "H", "Q", "R", "S", "T", "U", "V", "W", "X", "CA", "DA", "EA", "FA"],
          "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 0.0, 0.0]
         }, {
          "chains": ["E", "F", "G", "H", "Q", "R", "S", "T", "U", "V", "W", "X", "CA", "DA", "EA", "FA"],
          "matrix": [[-0.5, -0.8660254038, 0.0], [0.8660254038, -0.5, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 0.0, 0.0]
         }, {
          "chains": ["E", "F", "G", "H", "Q", "R", "S", "T", "U", "V", "W", "X", "CA", "DA", "EA", "FA"],
          "matrix": [[-0.5, 0.8660254038, 0.0], [-0.8660254038, -0.5, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 0.0, 0.0]
         }]
        })
        self.assertEqual(data_dicts["mmtf"]["geometry"]["assemblies"][4], {
         "id": 5, "software": None, "delta_energy": None,
         "buried_surface_area": None, "surface_area": None,
         "transformations": [{
          "chains": ["E", "F", "G", "H", "Q", "R", "S", "T", "U", "V", "W", "X", "CA", "DA", "EA", "FA"],
          "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 0.0, 0.0]
         }, {
          "chains": ["E", "F", "G", "H", "Q", "R", "S", "T", "U", "V", "W", "X", "CA", "DA", "EA", "FA"],
          "matrix": [[-0.5, -0.8660254038, 0.0], [0.8660254038, -0.5, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 0.0, 0.0]
         }, {
          "chains": ["E", "F", "G", "H", "Q", "R", "S", "T", "U", "V", "W", "X", "CA", "DA", "EA", "FA"],
          "matrix": [[-0.5, 0.8660254038, 0.0], [-0.8660254038, -0.5, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 0.0, 0.0]
         }]
        })
        self.assertEqual(data_dicts["pdb"]["geometry"]["assemblies"][4], {
         "id": 5, "software": "PISA", "delta_energy": -332.0,
         "buried_surface_area": 21680.0, "surface_area": 12240.0,
         "transformations": [{
          "chains": ["E", "F", "G", "H"],
          "matrix": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 0.0, 0.0]
         }, {
          "chains": ["E", "F", "G", "H"],
          "matrix": [[-0.5, -0.866025, 0.0], [0.866025, -0.5, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 0.0, 0.0]
         }, {
          "chains": ["E", "F", "G", "H"],
          "matrix": [[-0.5, 0.866025, 0.0], [-0.866025, -0.5, 0.0], [0.0, 0.0, 1.0]],
          "vector": [0.0, 0.0, 0.0]
         }]
        })


    def test_1m4x_data_dict_geometry(self):
        # Assemblies with lots of transformations to create virus
        data_dicts = self.open("1m4x")
        self.assertEqual(len(data_dicts["cif"]["geometry"]["assemblies"]), 7)
        self.assertEqual(len(data_dicts["mmtf"]["geometry"]["assemblies"]), 7)
        self.assertEqual(len(data_dicts["pdb"]["geometry"]["assemblies"]), 1)
        self.assertEqual(len(data_dicts["cif"]["geometry"]["assemblies"][2]["transformations"]), 140)
        self.assertEqual(len(data_dicts["cif"]["geometry"]["assemblies"][3]["transformations"]), 168)
        self.assertEqual(len(data_dicts["cif"]["geometry"]["assemblies"][4]["transformations"]), 30)
        self.assertEqual(len(data_dicts["cif"]["geometry"]["assemblies"][5]["transformations"]), 66)
        self.assertEqual(len(data_dicts["mmtf"]["geometry"]["assemblies"][2]["transformations"]), 140)
        self.assertEqual(len(data_dicts["mmtf"]["geometry"]["assemblies"][3]["transformations"]), 168)
        self.assertEqual(len(data_dicts["mmtf"]["geometry"]["assemblies"][4]["transformations"]), 30)
        self.assertEqual(len(data_dicts["mmtf"]["geometry"]["assemblies"][5]["transformations"]), 66)
        for d in data_dicts.values():
            self.assertEqual(len(d["geometry"]["assemblies"][0]["transformations"]), 1680)
            self.assertEqual(
             d["geometry"]["assemblies"][0]["transformations"][29]["chains"],
             ["A", "B", "C"]
            )
            self.assertAlmostEqual(
             d["geometry"]["assemblies"][0]["transformations"][29]["vector"][0],
             -18.95, delta=0.005
            )
            self.assertAlmostEqual(
             d["geometry"]["assemblies"][0]["transformations"][29]["matrix"][0][0],
             0.812, delta=0.005
            )
            self.assertAlmostEqual(
             d["geometry"]["assemblies"][0]["transformations"][29]["matrix"][-1][-1],
             0.286, delta=0.005
            )
        

    def test_4opj_data_dict_geometry(self):
        # Weird assemblies
        data_dicts = self.open("4opj")
        for d in data_dicts.values():
            self.assertEqual(len(d["geometry"]["assemblies"]), 2)
            self.assertEqual(d["geometry"]["assemblies"][0]["transformations"][0]["vector"], [42.387, 0, 0])