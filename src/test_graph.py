"""
Graph Theory Project - Test Suite
Author: Muhammad Mahdi Amirpour (m-amirpour)
Created at: 2025-06-14 10:58:43 UTC
"""

import unittest
from typing import Dict, List, Tuple
from graph_algorithm import GraphSequenceAnalyzer

class TestCases:
    """Collection of test cases for graph sequence analysis with detailed explanations"""
    
    @staticmethod
    def get_test_cases() -> Dict[str, Tuple[List[int], str, bool]]:
        """
        Returns a dictionary of test cases with their descriptions and expected results.
        Format: {name: (sequence, description, is_graphic)}
        """
        return {
            "Regular Graph (2,2,2,2)": (
                [2, 2, 2, 2],
                "A 2-regular graph where each vertex has exactly two neighbors. This forms a "
                "cycle graph C4 (cycle of length 4). In a regular graph, every vertex has the "
                "same degree. This sequence has exactly one possible realization due to its "
                "regularity and size. The sum of degrees is 8, which satisfies the handshaking "
                "lemma (sum of degrees = 2|E|, where |E| is the number of edges).",
                True
            ),
            "Star Graph (3,1,1,1)": (
                [3, 1, 1, 1],
                "A star graph K1,3 (also known as S4) with one central vertex of degree 3 "
                "connected to three leaves (vertices of degree 1). Star graphs are important in "
                "network design and are examples of complete bipartite graphs. This sequence "
                "has exactly one possible realization. Star graphs minimize the number of edges "
                "needed to ensure all vertices are connected.",
                True
            ),
            "Path Graph (2,2,1,1)": (
                [2, 2, 1, 1],
                "A path graph P4 of 4 vertices. The two vertices of degree 1 are the endpoints, "
                "while the two vertices of degree 2 form the internal path. This sequence has "
                "multiple possible realizations, demonstrating that different graphs can have "
                "the same degree sequence. Path graphs are fundamental in graph theory and "
                "represent linear arrangements of vertices.",
                True
            ),
            "Complete Graph K4 (3,3,3,3)": (
                [3, 3, 3, 3],
                "A complete graph K4 where every vertex is connected to all other vertices. "
                "In a complete graph of n vertices, each vertex has degree n-1. This sequence "
                "has exactly one possible realization due to the maximum connectivity requirement. "
                "Complete graphs represent networks with all possible edges present.",
                True
            ),
            "Complete Bipartite K2,3 (3,3,2,2,2)": (
                [3, 3, 2, 2, 2],
                "A complete bipartite graph K2,3 with partite sets of sizes 2 and 3. The two "
                "vertices in one set each have degree 3 (connected to all vertices in the other set), "
                "while the three vertices in the other set each have degree 2. This graph type is "
                "important in matching problems and network design. Has multiple possible realizations "
                "due to different ways of arranging the connections.",
                True
            ),
            "Wheel Graph W5 (4,3,3,3,3)": (
                [4, 3, 3, 3, 3],
                "A wheel graph W5 consisting of a central vertex (hub) connected to all vertices "
                "of a cycle graph C4. The hub has degree 4, while the rim vertices each have "
                "degree 3 (two neighbors on the rim plus the hub). Wheel graphs combine properties "
                "of star graphs and cycle graphs. Has exactly one possible realization due to "
                "its specific structure.",
                True
            ),
            "Tree Graph (3,1,1,1,1,1)": (
                [3, 1, 1, 1, 1, 1],
                "A tree with one vertex of degree 3 and five leaves. Trees are connected graphs "
                "without cycles. This sequence represents a star-like tree where one vertex "
                "connects to three leaves, and two more leaves connect to create branches. Has "
                "multiple possible realizations due to different ways of arranging the branches. "
                "Trees are fundamental in hierarchical structures.",
                True
            ),
            "Ladder Graph (3,3,3,3,2,2)": (
                [3, 3, 3, 3, 2, 2],
                "A ladder graph (P2 × P3) consisting of two parallel paths connected by rungs. "
                "The four vertices of degree 3 form the internal structure, while the two "
                "vertices of degree 2 are the endpoints. Ladder graphs are examples of graph "
                "products and have applications in chemical structures. Has multiple possible "
                "realizations.",
                True
            ),
            "Prism Graph (3,3,3,3,3,3)": (
                [3, 3, 3, 3, 3, 3],
                "A triangular prism graph (Y3) where each vertex has exactly three neighbors. "
                "This 3-regular graph consists of two triangles connected by three edges. "
                "Prism graphs are examples of polyhedral graphs and have applications in "
                "3D modeling. Has multiple possible realizations due to different ways of "
                "connecting the triangles.",
                True
            ),
            "Non-graphic Odd Sum (3,3,3,1)": (
                [3, 3, 3, 1],
                "Not a graphic sequence due to violation of degree sum property. The sum of "
                "degrees is 10 (odd), which contradicts the handshaking lemma stating that "
                "the sum must be even (twice the number of edges). This is a fundamental "
                "constraint in graph theory - no graph can have an odd sum of degrees.",
                False
            ),
            "Invalid High Degree (5,1,1,1)": (
                [5, 1, 1, 1],
                "Invalid sequence where one vertex has degree 5, which exceeds the number "
                "of possible connections (n-1 = 3) in a graph with 4 vertices. This violates "
                "the basic principle that in a simple graph, a vertex cannot have more "
                "neighbors than there are other vertices.",
                False
            ),
            "Self-Loop Required (3,1,0)": (
                [3, 1, 0],
                "Not realizable as a simple graph because it would require self-loops. "
                "The vertex of degree 3 cannot connect enough times to the vertex of "
                "degree 1 and the isolated vertex (degree 0). Simple graphs do not allow "
                "self-loops or multiple edges between the same vertices.",
                False
            ),
            "Multiple Edges Required (4,4,1)": (
                [4, 4, 1],
                "Not realizable as a simple graph because it would require multiple edges "
                "between the same vertices. The two vertices of degree 4 cannot satisfy their "
                "degree requirements without creating parallel edges, which are not allowed "
                "in simple graphs.",
                False
            ),
            "Empty Graph (0,0,0)": (
                [0, 0, 0],
                "A null graph (empty graph) with three isolated vertices. While this is a "
                "valid graph sequence, it represents the trivial case where no edges exist. "
                "Has exactly one possible realization. Empty graphs are important in studying "
                "graph complements and as base cases in algorithms.",
                True
            ),
            "Single Edge (1,1,0)": (
                [1, 1, 0],
                "A graph with one edge connecting two vertices and one isolated vertex. "
                "This is one of the simplest non-trivial graph sequences. Has exactly one "
                "possible realization. Demonstrates the concept of connected components in "
                "graph theory.",
                True
            )
        }

class TestGraphSequenceAnalyzer(unittest.TestCase):
    """Test suite for GraphSequenceAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = GraphSequenceAnalyzer()
        self.test_cases = TestCases.get_test_cases()

    def test_havel_hakimi(self):
        """Test sequences using Havel-Hakimi algorithm"""
        for name, (sequence, _, expected_result) in self.test_cases.items():
            with self.subTest(name=name):
                result = self.analyzer.is_graphic(sequence, method='havel-hakimi')
                self.assertEqual(
                    result,
                    expected_result,
                    f"Havel-Hakimi test failed for {name}"
                )

    def test_erdos_gallai(self):
        """Test sequences using Erdős-Gallai theorem"""
        for name, (sequence, _, expected_result) in self.test_cases.items():
            with self.subTest(name=name):
                result = self.analyzer.is_graphic(sequence, method='erdos-gallai')
                self.assertEqual(
                    result,
                    expected_result,
                    f"Erdős-Gallai test failed for {name}"
                )

    def test_both_methods(self):
        """Test sequences using both methods"""
        for name, (sequence, _, expected_result) in self.test_cases.items():
            with self.subTest(name=name):
                result = self.analyzer.is_graphic(sequence, method='both')
                self.assertEqual(
                    result,
                    expected_result,
                    f"Combined methods test failed for {name}"
                )

    def test_graph_generation(self):
        """Test graph generation for graphic sequences"""
        for name, (sequence, _, is_graphic) in self.test_cases.items():
            with self.subTest(name=name):
                if is_graphic:
                    graphs = self.analyzer.generate_all_graphs(sequence)
                    self.assertGreater(
                        len(graphs),
                        0,
                        f"No graphs generated for graphic sequence {name}"
                    )
                    
                    # Verify degrees in generated graphs
                    for graph in graphs:
                        degrees = sorted(
                            [d for _, d in graph.degree()],
                            reverse=True
                        )
                        self.assertEqual(
                            degrees,
                            sorted(sequence, reverse=True),
                            f"Generated graph degrees don't match for {name}"
                        )

    def test_empty_sequence(self):
        """Test empty sequence"""
        self.assertTrue(
            self.analyzer.is_graphic([]),
            "Empty sequence should be considered graphic"
        )

    def test_single_vertex(self):
        """Test single vertex with degree 0"""
        self.assertTrue(
            self.analyzer.is_graphic([0]),
            "Single vertex with degree 0 should be graphic"
        )

if __name__ == '__main__':
    unittest.main()