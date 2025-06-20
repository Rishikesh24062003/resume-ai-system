
import json
import logging
class TrieNode:
    """Optimized Trie node using __slots__ for memory efficiency"""
    __slots__ = ['children', 'is_end', 'metadata']
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.metadata = None
class SkillTrie:
    """Trie data structure for efficient skill matching and fuzzy search"""
    def __init__(self):
        self.root = TrieNode()
        self.skill_count = 0
    def insert(self, skill, metadata=None):
        """Insert a skill into the trie with optional metadata"""
        node = self.root
        for char in skill.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        if not node.is_end:
            self.skill_count += 1
        node.is_end = True
        node.metadata = metadata
    def search(self, skill):
        """Search for exact skill match"""
        node = self.root
        for char in skill.lower():
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    def fuzzy_search(self, term, max_distance=1):
        """Fuzzy search with Levenshtein distance"""
        results = []
        def dfs(node, current_word, remaining_term, distance):
            if distance > max_distance:
                return
            if node.is_end and distance <= max_distance:
                results.append((current_word, distance))
            if not remaining_term:
                # Only insertions left
                for char, child_node in node.children.items():
                    dfs(child_node, current_word + char, "", distance + 1)
                return
            current_char = remaining_term[0]
            remaining = remaining_term[1:]
            # Exact match
            if current_char in node.children:
                dfs(node.children[current_char], current_word + current_char, remaining, distance)
            # Substitution
            for char, child_node in node.children.items():
                if char != current_char:
                    dfs(child_node, current_word + char, remaining, distance + 1)
            # Insertion
            for char, child_node in node.children.items():
                dfs(child_node, current_word + char, remaining_term, distance + 1)
            # Deletion
            dfs(node, current_word, remaining, distance + 1)
        dfs(self.root, "", term.lower(), 0)
        return sorted(results, key=lambda x: x[1])[:5]
    def load_skills_from_file(self, file_path):
        """Load skills from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                skills_data = json.load(f)
                for skill_item in skills_data:
                    if isinstance(skill_item, dict):
                        skill = skill_item.get('skill', '')
                        category = skill_item.get('category', 'general')
                        self.insert(skill, {'category': category})
                    else:
                        self.insert(str(skill_item))
                logging.info(f"Loaded {self.skill_count} skills from {file_path}")
        except Exception as e:
            logging.error(f"Error loading skills: {e}")
    def get_all_skills(self):
        """Get all skills in the trie"""
        skills = []
        def dfs(node, current_word):
            if node.is_end:
                skills.append(current_word)
            for char, child_node in node.children.items():
                dfs(child_node, current_word + char)
        dfs(self.root, "")
        return skills

