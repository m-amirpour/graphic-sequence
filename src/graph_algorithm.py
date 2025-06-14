from typing import List, Set, Dict, Tuple
import networkx as nx
from itertools import combinations

class GraphSequenceAnalyzer:
    """
    A class for analyzing graphic sequences using both Havel-Hakimi and Erdős-Gallai theorems.
    """
    
    def erdos_gallai_check(self, sequence: List[int]) -> bool:
        """
        Implements the Erdős-Gallai theorem to check if a sequence is graphic.
        
        The Erdős-Gallai theorem states that a sequence of non-negative integers 
        d1 ≥ d2 ≥ ... ≥ dn is graphic if and only if its sum is even and
        
        sum(di) <= k(k-1) + sum(min(di,k)) for all k in [1,n]
                                          i=k+1
        
        Args:
            sequence (List[int]): A sequence of non-negative integers
            
        Returns:
            bool: True if the sequence is graphic, False otherwise
        """
        if not sequence:
            return True
            
        # Make a copy and sort in descending order
        seq = sorted(sequence, reverse=True)
        n = len(seq)
        
        # Check if sum is even
        if sum(seq) % 2 != 0:
            return False
            
        # Check Erdős-Gallai conditions
        for k in range(1, n + 1):
            left_sum = sum(seq[:k])
            right_sum = k * (k - 1)
            right_sum += sum(min(seq[i], k) for i in range(k, n))
            
            if left_sum > right_sum:
                return False
                
        return True
        
    def havel_hakimi_check(self, sequence: List[int]) -> bool:
        """
        Implements the Havel-Hakimi theorem to check if a sequence is graphic.
        
        Args:
            sequence (List[int]): A sequence of non-negative integers
            
        Returns:
            bool: True if the sequence is graphic, False otherwise
        """
        if not sequence:
            return True
        
        # Make a copy to avoid modifying the original sequence
        seq = sequence.copy()
        
        while True:
            # Sort in descending order
            seq.sort(reverse=True)
            
            # If all elements are 0, the sequence is graphic
            if all(x == 0 for x in seq):
                return True
            
            # Get the first element
            d1 = seq.pop(0)
            
            # If d1 is negative or greater than available vertices,
            # the sequence is not graphic
            if d1 < 0 or d1 >= len(seq):
                return False
                
            # Subtract 1 from the next d1 elements
            for i in range(d1):
                if i >= len(seq):
                    return False
                seq[i] -= 1
                
    def is_graphic(self, sequence: List[int], method: str = 'both') -> bool:
        """
        Determines if a sequence is graphic using specified method(s).
        
        Args:
            sequence (List[int]): A sequence of non-negative integers
            method (str): Which method to use - 'havel-hakimi', 'erdos-gallai', or 'both'
            
        Returns:
            bool: True if the sequence is graphic, False otherwise
        """
        if method.lower() == 'havel-hakimi':
            return self.havel_hakimi_check(sequence)
        elif method.lower() == 'erdos-gallai':
            return self.erdos_gallai_check(sequence)
        else:  # Use both methods as a double-check
            return (self.havel_hakimi_check(sequence) and 
                   self.erdos_gallai_check(sequence))

    def generate_all_graphs(self, sequence: List[int]) -> List[nx.Graph]:
        """
        Generates all possible non-isomorphic simple graphs with the given degree sequence.
        
        Args:
            sequence (List[int]): A graphic sequence
            
        Returns:
            List[nx.Graph]: List of all non-isomorphic graphs with the given degree sequence
        """
        if not self.is_graphic(sequence):
            return []

        n = len(sequence)
        vertices = list(range(n))
        result_graphs = []
        
        # Generate all possible edge combinations
        potential_edges = list(combinations(vertices, 2))
        
        def is_valid_graph(edges: Set[Tuple[int, int]]) -> bool:
            """Check if a set of edges creates a graph with the desired degree sequence."""
            degrees = [0] * n
            for u, v in edges:
                degrees[u] += 1
                degrees[v] += 1
            return sorted(degrees, reverse=True) == sorted(sequence, reverse=True)

        def generate_graphs(current_edges: Set[Tuple[int, int]], 
                          remaining_edges: List[Tuple[int, int]], 
                          vertex_degrees: List[int]):
            """Recursively generate all possible valid graphs."""
            if is_valid_graph(current_edges):
                G = nx.Graph()
                G.add_nodes_from(vertices)
                G.add_edges_from(current_edges)
                
                # Check if this graph is isomorphic to any existing graph
                if not any(nx.is_isomorphic(G, H) for H in result_graphs):
                    result_graphs.append(G)
                return

            if not remaining_edges:
                return

            edge = remaining_edges[0]
            new_remaining = remaining_edges[1:]
            
            # Try adding the edge
            new_degrees = vertex_degrees.copy()
            new_degrees[edge[0]] += 1
            new_degrees[edge[1]] += 1
            
            if all(d <= s for d, s in zip(new_degrees, sequence)):
                generate_graphs(
                    current_edges | {edge},
                    new_remaining,
                    new_degrees
                )
            
            # Try without adding the edge
            generate_graphs(
                current_edges,
                new_remaining,
                vertex_degrees
            )

        generate_graphs(set(), potential_edges, [0] * n)
        return result_graphs