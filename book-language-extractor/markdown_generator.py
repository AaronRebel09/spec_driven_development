def generate_chapter_markdown(chapter, extractor_result, difficulty="Medium"):
    lines = []

    # Chapter Title Heading
    lines.append(f"# {chapter.get('title', 'Untitled Chapter')}")
    lines.append("")

    glossary = extractor_result.get('glossary', [])
    idioms = extractor_result.get('idioms', [])
    phrasal_verbs = extractor_result.get('phrasal_verbs', [])
    slangs = extractor_result.get('slangs', [])
    all_phrases = extractor_result.get('phrases', [])

    # Add glossary section
    if glossary:
        lines.extend([
            "## Glossary",

            "| Term | POS | Definition | Spanish | Example | Difficulty |",
            "|--------|-----|-----------|---------|---------|------------|"
        ])
        for word_data in glossary:
            term = word_data.get('term', 'N/A')
            pos = word_data.get('pos', 'n/a')
            definition = word_data.get('definition', '')
            spanish = word_data.get('spanish', '[No Spanish]')
            context_sents = word_data.get('context_sentences', [])
            example = context_sents[0][:55] + "..." if len(context_sents) > 0 and context_sents[0] else 'See full text'

            # Ensure proper spacing in columns
            clean_term = term.replace('|', '\\|')
            clean_pos = pos.replace('|', '\\|')
            clean_def = definition[:45] + "..." if len(definition) > 45 else definition
            clean_example = example.replace('|', '\\|')

            line = f"| {clean_term} | {clean_pos} | {clean_def} | {spanish} | {clean_example} | {difficulty} |"
            lines.append(line)
        lines.append("")

    # Add idioms section if found
    if idioms:
        lines.extend([
            "## Idioms & Expressions",

            "| Phrase | Meaning | Spanish | Example | Type |",
            "|--------|---------|---------|---------|------|"
        ])
        for idiom in idioms:
            phrase = idiom.get('phrase', 'N/A')
            meaning = idiom.get('meaning', '')
            spanish = idiom.get('spanish', '[Sin traducción]')
            example = idiom.get('example', 'See chapter text')[:45] + "..." if len(idiom.get('example', '')) > 45 else idiom.get('example', '')

            clean_phrase = phrase.replace('|', '\\|')

            line = f"| {clean_phrase} | {meaning} | {spanish} | {example} | {idiom.get('type', 'idiom')} |"
            lines.append(line)

        lines.append("")

    # Add phrasal verbs section if found
    if phrasal_verbs:
        lines.extend([
            "## Phrasal Verbs",

            "| Phrase | Meaning | Spanish | Example | Type |",
            "|--------|---------|---------|---------|------|"
        ])
        for pv in phrasal_verbs:
            phrase = pv.get('phrase', 'N/A')
            meaning = pv.get('meaning', '')
            spanish = pv.get('spanish', '[Sin traducción]')
            example = pv.get('example', 'See chapter text')[:45] + "..." if len(pv.get('example', '')) > 45 else pv.get('example', '')

            clean_phrase = phrase.replace('|', '\\|')

            line = f"| {clean_phrase} | {meaning} | {spanish} | {example} | {pv.get('type', 'phrasal_verb')} |"
            lines.append(line)

        lines.append("")

    # Add slangs section if found
    if slangs:
        lines.extend([
            "## Slang & Colloquial Expressions",

            "| Expression | Meaning | Spanish | Example | Type |",
            "|------------|---------|---------|---------|------|"
        ])
        for slang in slangs:
            phrase = slang.get('phrase', 'N/A')
            meaning = slang.get('meaning', '')
            spanish = slang.get('spanish', '[Sin traducción]')
            example = slang.get('example', 'See chapter text')[:45] + "..." if len(slang.get('example', '')) > 45 else slang.get('example', '')

            clean_phrase = phrase.replace('|', '\\|')

            line = f"| {clean_phrase} | {meaning} | {spanish} | {example} | {slang.get('type', 'slang')} |"
            lines.append(line)

        lines.append("")

    # Add phrases section if found
    if all_phrases:
        lines.extend([
            "## Dynamic Phrases",

            "| Phrase | Meaning | Spanish | Example | Type |",
            "|--------|---------|---------|---------|------|"
        ])
        for p in all_phrases:
            phrase = p.get('phrase', 'N/A')
            meaning = p.get('meaning', '')
            spanish = p.get('spanish', '[No translation]')
            example = p.get('example', 'See chapter text')[:45] + "..." if len(p.get('example', '')) > 45 else p.get('example', '')

            clean_phrase = phrase.replace('|', '\\|')

            line = f"| {clean_phrase} | {meaning} | {spanish} | {example} | {p.get('type', 'phrase')} |"
            lines.append(line)

        lines.append("")

    # Add Review section
    top_terms = [g['term'].capitalize() for g in glossary[:6]]
    keyword_str = ", ".join(top_terms) if top_terms else "No specific terms yet."

    lines.extend([
        "## Review & Notes",

        "- **Key themes:** Important terms and concepts from this chapter.",

        "",
        f"- **Priority vocabulary to memorize first:** {keyword_str}",

        "",
        "- **Cultural notes:**",
        "  - Idioms and phrasal verbs have cultural nuances in each language.",
        "  - Spanish translations are provided where available.",
        "",
        "---",

        "",
        "*Extracted from: book.md*",
        f"*Chapter reference: {chapter.get('chapter_id', 'N/A')}*"
    ])

    return "\n".join(lines)
