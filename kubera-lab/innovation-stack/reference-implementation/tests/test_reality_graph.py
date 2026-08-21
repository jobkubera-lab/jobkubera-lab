import unittest
from kubera_innovation.reality_graph import RealityGraph

class RealityGraphTests(unittest.TestCase):
    def setUp(self): self.g=RealityGraph()
    def tearDown(self): self.g.close()
    def test_add_and_get_node(self): self.g.add_node("p1","Project","Project One"); self.assertEqual(self.g.get_node("p1").label,"Project One")
    def test_invalid_visibility(self):
        with self.assertRaises(ValueError): self.g.add_node("p1","Project","P",visibility="SECRET")
    def test_edge_requires_existing_nodes(self):
        self.g.add_node("p1","Project","P")
        with self.assertRaises(KeyError): self.g.add_edge("p1","USES","missing")
    def test_neighbors(self):
        self.g.add_node("a","Idea","A"); self.g.add_node("b","Project","B"); self.g.add_edge("a","CREATED_FROM","b"); self.assertEqual([n.node_id for n in self.g.neighbors("a")],["b"])
    def test_public_export_excludes_private(self):
        self.g.add_node("pub","Place","Public",visibility="PUBLIC"); self.g.add_node("priv","Note","Private",visibility="PRIVATE"); self.assertEqual([n["id"] for n in self.g.export_public()["nodes"]],["pub"])
    def test_public_export_excludes_edge_to_private(self):
        self.g.add_node("pub","Place","Public",visibility="PUBLIC"); self.g.add_node("priv","Note","Private",visibility="PRIVATE"); self.g.add_edge("pub","RELATED_TO","priv"); self.assertEqual(self.g.export_public()["edges"],[])

if __name__ == "__main__": unittest.main()
