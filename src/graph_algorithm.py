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
        
        while seq:  # Changed from while True
            # Sort in descending order
            seq.sort(reverse=True)
            
            # If all elements are 0, the sequence is graphic
            if all(x == 0 for x in seq):
                return True
            
            # Get the first element
            d1 = seq.pop(0)
            
            # If d1 is negative or strictly greater than available vertices,
            # the sequence is not graphic
            if d1 < 0 or d1 > len(seq):  # Changed from d1 >= len(seq)
                return False
                
            # Subtract 1 from the next d1 elements
            for i in range(d1):
                if i >= len(seq):  # This check may not be needed with fixed condition above
                    return False
                seq[i] -= 1
        
        return True  # Added return True for case when sequence becomes empty
        
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
        
        # Create a graph with the correct number of vertices
        G = nx.Graph()
        G.add_nodes_from(vertices)
        
        def is_valid_degree_sequence(G):
            """Check if the current graph has the desired degree sequence"""
            current_degrees = sorted([G.degree(v) for v in G.nodes()], reverse=True)
            target_degrees = sorted(sequence, reverse=True)
            return current_degrees == target_degrees

        def can_add_edge(G, u, v, target_degrees):
            """Check if adding edge (u,v) maintains valid degree sequence"""
            if G.has_edge(u, v):
                return False
            return (G.degree(u) < target_degrees[u] and 
                    G.degree(v) < target_degrees[v])

        def generate_recursive(G, remaining_edges):
            if is_valid_degree_sequence(G):
                # Found a valid graph
                if not any(nx.is_isomorphic(G, H) for H in result_graphs):
                    result_graphs.append(G.copy())
                return

            if not remaining_edges:
                return

            u, v = remaining_edges[0]
            new_remaining = remaining_edges[1:]

            # Try adding the edge
            if can_add_edge(G, u, v, dict(zip(vertices, sequence))):
                G.add_edge(u, v)
                generate_recursive(G, new_remaining)
                G.remove_edge(u, v)

            # Try without the edge
            generate_recursive(G, new_remaining)

        # Generate all possible edge combinations
        potential_edges = list(combinations(vertices, 2))
        generate_recursive(G, potential_edges)
        
        return result_graphs
