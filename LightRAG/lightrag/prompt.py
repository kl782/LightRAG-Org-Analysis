GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

# Modified to focus on organization-related entities
PROMPTS["DEFAULT_ENTITY_TYPES"] = ["organization", "business_unit", "market", "product", "technology", "location"]

PROMPTS["entity_extraction"] = """-Goal-
Given text content about an organization (typically from their website or public documents), identify all relevant business entities and their relationships. Focus on understanding the organization's structure, offerings, and market position.
Use {language} as output language.

-Steps-
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalize the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: For organizations: core business, size, and value proposition
                     For markets: size, growth, and key characteristics
                     For products: features, benefits, and target users
                     For technology: capabilities, maturity, and use cases
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that show business relationships.
For each pair of related entities, extract:
- source_entity: name of the source entity
- target_entity: name of the target entity
- relationship_description: business relationship between entities
- relationship_strength: numeric score (1-10) indicating relationship importance
- relationship_keywords: key business concepts that characterize the relationship
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify business-focused keywords that describe:
- Core value proposition
- Market positioning
- Technological capabilities
- Growth indicators
Format as ("content_keywords"{tuple_delimiter}<business_keywords>)

4. Return output in {language} as a list using **{record_delimiter}** as delimiter.

5. When finished, output {completion_delimiter}

Special Instructions:
- Focus on concrete business information over general descriptions
- Prioritize quantifiable information (employee counts, market sizes, etc.)
- Note relationships between organizations and markets/technologies
- Identify any stated or implied value propositions
- Extract information about organizational readiness and capabilities
- Look for indicators of market position and competitive advantages

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:
"""

# Modified example to focus on business entities
PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types: [organization, business_unit, market, product, technology]
Text:
Acme Solutions, a leading enterprise software provider with over 5,000 employees globally, specializes in AI-powered automation solutions. Their flagship product, AutomateX, leverages advanced machine learning to streamline business processes. The company operates primarily in the financial services and healthcare markets, where regulatory compliance is a key concern. Their R&D division, consisting of 200 AI researchers, continually enhances their core ML technology platform.
################
Output:
("entity"{tuple_delimiter}"Acme Solutions"{tuple_delimiter}"organization"{tuple_delimiter}"Enterprise software provider with 5,000 global employees, focused on AI-powered automation"){record_delimiter}
("entity"{tuple_delimiter}"AutomateX"{tuple_delimiter}"product"{tuple_delimiter}"Flagship automation product using machine learning for business process optimization"){record_delimiter}
("entity"{tuple_delimiter}"R&D Division"{tuple_delimiter}"business_unit"{tuple_delimiter}"200-person research team focused on AI and ML development"){record_delimiter}
("entity"{tuple_delimiter}"Financial Services Market"{tuple_delimiter}"market"{tuple_delimiter}"Key target market with emphasis on regulatory compliance"){record_delimiter}
("entity"{tuple_delimiter}"Healthcare Market"{tuple_delimiter}"market"{tuple_delimiter}"Key target market with emphasis on regulatory compliance"){record_delimiter}
("entity"{tuple_delimiter}"ML Technology Platform"{tuple_delimiter}"technology"{tuple_delimiter}"Core machine learning platform supporting automation solutions"){record_delimiter}
("relationship"{tuple_delimiter}"Acme Solutions"{tuple_delimiter}"AutomateX"{tuple_delimiter}"Acme develops and offers AutomateX as their main product"{tuple_delimiter}"product development, market offering"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"AutomateX"{tuple_delimiter}"ML Technology Platform"{tuple_delimiter}"AutomateX is built on and powered by the ML platform"{tuple_delimiter}"technology dependency, product architecture"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"R&D Division"{tuple_delimiter}"ML Technology Platform"{tuple_delimiter}"R&D team develops and enhances the ML platform"{tuple_delimiter}"research, development, innovation"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"enterprise software, AI automation, regulatory compliance, machine learning, global operations"){completion_delimiter}
""",
]

# [Rest of the PROMPTS dictionary remains unchanged]
