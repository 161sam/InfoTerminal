"""Relation extraction module for InfoTerminal doc-entities service."""

import logging
import re
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional, Tuple

import spacy


class RelationExtractor:
    """Extract relationships between entities using spaCy dependency parsing and patterns."""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the relation extractor with spaCy model."""

        self.logger = logging.getLogger(__name__)
        self.supports_dependencies = False

        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            self.logger.warning(
                "spaCy model %s missing – falling back to blank('en') pipeline",
                model_name,
            )
            self.nlp = spacy.blank("en")
        except Exception as exc:  # pragma: no cover - defensive guard
            self.logger.warning("spaCy load error (%s); using blank pipeline", exc)
            self.nlp = spacy.blank("en")

        if not hasattr(self.nlp, "has_pipe"):
            original_nlp = self.nlp

            class _CallablePipeline:
                def __init__(self, func):
                    self._func = func

                def __call__(self, text: str):  # pragma: no cover - exercised in tests
                    return self._func(text)

                def has_pipe(self, _: str) -> bool:
                    return False

                def add_pipe(self, *_args, **_kwargs):  # pragma: no cover - no-op in stubs
                    return None

            self.nlp = _CallablePipeline(original_nlp)

        if not self.nlp.has_pipe("sentencizer"):
            try:
                self.nlp.add_pipe("sentencizer")
            except Exception:  # pragma: no cover - spaCy <3.1 fallback
                pass

        self.supports_dependencies = self.nlp.has_pipe("parser")
        
        # Relation patterns for different entity types
        self.relation_patterns = {
            "PERSON_ORG": {
                "WORKS_AT": [
                    {"verbs": ["work", "works", "worked", "working"], "preps": ["at", "for", "with"]},
                    {"verbs": ["employ", "employs", "employed"], "preps": ["by", "at"]},
                    {"verbs": ["join", "joins", "joined"], "preps": []},
                    {"patterns": [r"(.+) of (.+)", r"(.+) at (.+)", r"(.+) from (.+)"]}
                ],
                "LEADS": [
                    {"verbs": ["lead", "leads", "led", "leading"], "preps": []},
                    {"verbs": ["head", "heads", "headed"], "preps": []},
                    {"verbs": ["manage", "manages", "managed"], "preps": []},
                    {"patterns": [r"CEO of (.+)", r"director of (.+)", r"manager of (.+)"]}
                ],
                "FOUNDED": [
                    {"verbs": ["found", "founded", "establish", "established"], "preps": []},
                    {"verbs": ["create", "created", "start", "started"], "preps": []},
                    {"patterns": [r"founder of (.+)", r"co-founder of (.+)"]}
                ]
            },
            "PERSON_GPE": {
                "BORN_IN": [
                    {"verbs": ["born"], "preps": ["in", "at"]},
                    {"patterns": [r"born in (.+)", r"native of (.+)", r"from (.+)"]}
                ],
                "LIVES_IN": [
                    {"verbs": ["live", "lives", "lived", "residing"], "preps": ["in", "at"]},
                    {"patterns": [r"resident of (.+)", r"based in (.+)"]}
                ],
                "VISITED": [
                    {"verbs": ["visit", "visited", "travel", "traveled"], "preps": ["to"]},
                    {"patterns": [r"trip to (.+)", r"journey to (.+)"]}
                ]
            },
            "ORG_GPE": {
                "LOCATED_IN": [
                    {"verbs": ["located"], "preps": ["in", "at"]},
                    {"verbs": ["based"], "preps": ["in", "at"]},
                    {"patterns": [r"headquarters in (.+)", r"office in (.+)"]}
                ],
                "OPERATES_IN": [
                    {"verbs": ["operate", "operates", "operated"], "preps": ["in", "at"]},
                    {"patterns": [r"presence in (.+)", r"operations in (.+)"]}
                ]
            },
            "PERSON_PERSON": {
                "KNOWS": [
                    {"verbs": ["know", "knows", "knew"], "preps": []},
                    {"verbs": ["meet", "meets", "met"], "preps": []},
                    {"patterns": [r"friend of (.+)", r"colleague of (.+)"]}
                ],
                "MARRIED_TO": [
                    {"verbs": ["marry", "married"], "preps": ["to"]},
                    {"patterns": [r"wife of (.+)", r"husband of (.+)", r"spouse of (.+)"]}
                ]
            }
        }
    
    def extract_relations(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract relations from text given a list of entities."""
        if not entities or len(entities) < 2:
            return []
        
        doc = self.nlp(text)
        relations = []
        
        # Create entity map for quick lookup
        entity_map = {}
        for entity in entities:
            for token_idx in range(entity.get("span_start", 0), entity.get("span_end", 0)):
                if token_idx < len(text):
                    entity_map[token_idx] = entity
        
        # Method 1: Dependency parsing (skip when parser unavailable)
        if self.supports_dependencies:
            dependency_relations = self._extract_dependency_relations(doc, entities)
            relations.extend(dependency_relations)
        
        # Method 2: Pattern matching
        pattern_relations = self._extract_pattern_relations(text, entities)
        relations.extend(pattern_relations)
        
        # Method 3: Sentence-level co-occurrence
        cooccurrence_relations = self._extract_cooccurrence_relations(doc, text, entities)
        relations.extend(cooccurrence_relations)
        
        # Remove duplicates and rank by confidence
        relations = self._deduplicate_relations(relations)
        
        return relations
    
    def _extract_dependency_relations(self, doc, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract relations using spaCy dependency parsing."""
        if not self.supports_dependencies:
            return []
        relations = []
        
        # Create token-to-entity mapping
        token_to_entity = {}
        for entity in entities:
            start_char = entity.get("span_start", 0)
            end_char = entity.get("span_end", 0)
            
            for token in doc:
                if token.idx >= start_char and token.idx < end_char:
                    token_to_entity[token.i] = entity
        
        # Analyze dependency tree for relations
        for token in doc:
            if token.pos_ == "VERB":
                # Find subjects and objects of the verb
                subjects = [child for child in token.children if child.dep_ in ["nsubj", "nsubjpass"]]
                objects = [child for child in token.children if child.dep_ in ["dobj", "pobj", "iobj"]]
                
                for subj in subjects:
                    for obj in objects:
                        subj_entity = self._find_entity_for_token(subj, token_to_entity)
                        obj_entity = self._find_entity_for_token(obj, token_to_entity)
                        
                        if subj_entity and obj_entity and subj_entity != obj_entity:
                            relation_type = self._classify_relation(
                                token.lemma_, 
                                subj_entity.get("label", ""), 
                                obj_entity.get("label", "")
                            )
                            
                            if relation_type:
                                relations.append({
                                    "subject_entity_id": subj_entity.get("id"),
                                    "object_entity_id": obj_entity.get("id"),
                                    "predicate": relation_type,
                                    "predicate_text": token.text,
                                    "confidence": 0.7,
                                    "span_start": token.idx,
                                    "span_end": token.idx + len(token.text),
                                    "context": self._get_sentence_context(token),
                                    "extraction_method": "dependency_parse",
                                    "metadata": {
                                        "verb": token.text,
                                        "lemma": token.lemma_,
                                        "pos": token.pos_,
                                        "dep": token.dep_
                                    }
                                })
        
        return relations
    
    def _extract_pattern_relations(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract relations using predefined patterns."""
        relations = []
        
        # Sort entities by position for processing
        sorted_entities = sorted(entities, key=lambda x: x.get("span_start", 0))
        
        for i, ent1 in enumerate(sorted_entities):
            for j, ent2 in enumerate(sorted_entities[i+1:], i+1):
                # Check if entities are close enough (within 50 characters)
                if ent2.get("span_start", 0) - ent1.get("span_end", 0) > 50:
                    continue
                
                # Extract text between entities
                between_text = text[ent1.get("span_end", 0):ent2.get("span_start", 0)]
                
                # Check patterns for entity type combination
                entity_combo = f"{ent1.get('label', '')}_{ent2.get('label', '')}"
                if entity_combo in self.relation_patterns:
                    for relation_type, patterns in self.relation_patterns[entity_combo].items():
                        if self._match_patterns(between_text, patterns):
                            relations.append({
                                "subject_entity_id": ent1.get("id"),
                                "object_entity_id": ent2.get("id"),
                                "predicate": relation_type,
                                "predicate_text": between_text.strip(),
                                "confidence": 0.8,
                                "span_start": ent1.get("span_end", 0),
                                "span_end": ent2.get("span_start", 0),
                                "context": text[max(0, ent1.get("span_start", 0)-30):min(len(text), ent2.get("span_end", 0)+30)],
                                "extraction_method": "pattern_match",
                                "metadata": {
                                    "pattern_matched": relation_type,
                                    "between_text": between_text.strip()
                                }
                            })
        
        return relations
    
    def _extract_cooccurrence_relations(
        self,
        doc,
        text: str,
        entities: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Extract relations based on co-occurrence in the same sentence."""
        relations = []

        # Group entities by sentence
        sentence_entities = defaultdict(list)
        sentences = list(self._iter_sentences(doc, text))
        for entity in entities:
            start_char = entity.get("span_start", 0)
            for sent_text, sent_start, sent_end in sentences:
                if sent_start <= start_char < sent_end:
                    sentence_entities[(sent_text, sent_start, sent_end)].append(entity)
                    break

        # For entities in the same sentence, infer weak relations
        for (sentence_text, _, _), sent_entities in sentence_entities.items():
            if len(sent_entities) >= 2:
                for i, ent1 in enumerate(sent_entities):
                    for ent2 in sent_entities[i+1:]:
                        # Only create weak relations for certain entity type combinations
                        if self._should_create_weak_relation(ent1.get("label", ""), ent2.get("label", "")):
                            relations.append({
                                "subject_entity_id": ent1.get("id"),
                                "object_entity_id": ent2.get("id"),
                                "predicate": "RELATED_TO",
                                "predicate_text": "co-occurrence",
                                "confidence": 0.3,
                                "span_start": min(ent1.get("span_start", 0), ent2.get("span_start", 0)),
                                "span_end": max(ent1.get("span_end", 0), ent2.get("span_end", 0)),
                                "context": sentence_text,
                                "extraction_method": "cooccurrence",
                                "metadata": {
                                    "sentence": sentence_text,
                                    "entity_distance": abs(ent1.get("span_start", 0) - ent2.get("span_start", 0))
                                }
                            })
        
        return relations
    
    def _find_entity_for_token(self, token, token_to_entity: Dict) -> Optional[Dict[str, Any]]:
        """Find entity that contains the given token."""
        # Check if token is directly mapped
        if token.i in token_to_entity:
            return token_to_entity[token.i]
        
        # Check if token is part of a multi-token entity
        for i in range(max(0, token.i - 3), min(len(token_to_entity), token.i + 4)):
            if i in token_to_entity:
                entity = token_to_entity[i]
                if (token.idx >= entity.get("span_start", 0) and 
                    token.idx < entity.get("span_end", 0)):
                    return entity
        
        return None
    
    def _classify_relation(self, verb: str, subj_label: str, obj_label: str) -> Optional[str]:
        """Classify relation type based on verb and entity labels."""
        verb = verb.lower()
        
        # Person-Organization relations
        if subj_label == "PERSON" and obj_label == "ORG":
            if verb in ["work", "employ", "join"]:
                return "WORKS_AT"
            elif verb in ["lead", "head", "manage", "run"]:
                return "LEADS"
            elif verb in ["found", "establish", "create", "start"]:
                return "FOUNDED"
        
        # Person-Location relations
        elif subj_label == "PERSON" and obj_label in ["GPE", "LOC"]:
            if verb in ["bear", "born"]:
                return "BORN_IN"
            elif verb in ["live", "reside"]:
                return "LIVES_IN"
            elif verb in ["visit", "travel"]:
                return "VISITED"
        
        # Organization-Location relations
        elif subj_label == "ORG" and obj_label in ["GPE", "LOC"]:
            if verb in ["locate", "base", "headquarter"]:
                return "LOCATED_IN"
            elif verb in ["operate", "business"]:
                return "OPERATES_IN"
        
        # Person-Person relations
        elif subj_label == "PERSON" and obj_label == "PERSON":
            if verb in ["know", "meet"]:
                return "KNOWS"
            elif verb in ["marry"]:
                return "MARRIED_TO"
        
        return None
    
    def _match_patterns(self, text: str, patterns: List[Dict]) -> bool:
        """Check if text matches any of the given patterns."""
        text = text.lower().strip()
        
        for pattern_group in patterns:
            if "verbs" in pattern_group:
                verbs = pattern_group["verbs"]
                preps = pattern_group.get("preps", [])
                
                for verb in verbs:
                    if verb in text:
                        if not preps:
                            return True
                        for prep in preps:
                            if prep in text:
                                return True
            
            if "patterns" in pattern_group:
                for pattern in pattern_group["patterns"]:
                    if re.search(pattern.lower(), text):
                        return True
        
        return False
    
    def _should_create_weak_relation(self, label1: str, label2: str) -> bool:
        """Determine if we should create a weak relation between entity types."""
        weak_relation_pairs = {
            ("PERSON", "ORG"), ("ORG", "PERSON"),
            ("PERSON", "GPE"), ("GPE", "PERSON"),
            ("PERSON", "LOC"), ("LOC", "PERSON"),
            ("ORG", "GPE"), ("GPE", "ORG"),
            ("ORG", "LOC"), ("LOC", "ORG")
        }
        return (label1, label2) in weak_relation_pairs
    
    def _get_sentence_context(self, token) -> str:
        """Get sentence context for a token."""
        try:
            sent = token.sent
            return sent.text.strip()
        except AttributeError:
            return ""

    def _iter_sentences(self, doc, text: str) -> Iterable[Tuple[str, int, int]]:
        """Yield sentence text and boundaries even without parser support."""

        if (
            doc is not None
            and hasattr(doc, "has_annotation")
            and hasattr(doc, "sents")
        ):
            try:
                if doc.has_annotation("SENT_START"):
                    for sent in doc.sents:
                        yield sent.text, sent.start_char, sent.end_char
                    return
            except Exception:  # pragma: no cover - defensive fallback
                pass

        if not text:
            return

        offset = 0
        for match in re.finditer(r"[^.!?]+[.!?]?", text):
            chunk = match.group().strip()
            if not chunk:
                continue
            start = match.start()
            end = match.end()
            offset = end
            yield chunk, start, end

        if offset < len(text):
            remainder = text[offset:].strip()
            if remainder:
                yield remainder, offset, len(text)
    
    def _deduplicate_relations(self, relations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate relations and keep the highest confidence ones."""
        # Group by entity pair and predicate
        relation_groups = defaultdict(list)
        
        for relation in relations:
            key = (
                relation["subject_entity_id"], 
                relation["object_entity_id"], 
                relation["predicate"]
            )
            relation_groups[key].append(relation)
        
        # Keep the highest confidence relation for each group
        deduplicated = []
        for group in relation_groups.values():
            best_relation = max(group, key=lambda x: x.get("confidence", 0))
            deduplicated.append(best_relation)
        
        # Sort by confidence
        return sorted(deduplicated, key=lambda x: x.get("confidence", 0), reverse=True)


# Create a global instance for reuse
relation_extractor = RelationExtractor()


def extract_relations(text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract relations from text given entities (convenience function)."""
    return relation_extractor.extract_relations(text, entities)
