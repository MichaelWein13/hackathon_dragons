# 🌐 MultiWikiCheck: Detecting Cross-Language Discrepancies on Wikipedia

**MultiWikiCheck** is a Chrome extension that analyzes Wikipedia articles across multiple languages to uncover contradictions and missing information. By translating and comparing different language versions of the same article, it helps surface underreported perspectives or facts that may otherwise remain hidden due to language barriers.

## 🚨 The Problem

Wikipedia is an invaluable knowledge resource, but the content of articles often varies significantly between languages. These discrepancies can lead to:

- Contradictory claims in different versions of the same article
- Missing facts or underreported viewpoints
- Biased understanding, especially for users who access content in only one language
- This tool aims to expose these inconsistencies to promote a more complete and balanced understanding of any given topic.

## ✅ Our Solution

MultiWikiCheck automates the process of comparing Wikipedia articles across languages by:

- Translating articles into a common language
- Aligning sections and sentences across versions
- Detecting contradictions, or inconsistencies
- Suggesting related sources or articles to help users explore flagged issues further
- Summarize those related sources

## 🧠 Technical Overview

The core of **MultiWikiCheck** is a multilingual analysis pipeline that performs the following steps:

1. **Data Collection**: Fetch articles on the same topic in different languages using the Wikipedia API.
2. **Translation & Normalization**: Translate all content into a pivot language (e.g., English) using a translation model or API.
3. **Discrepancy Detection**: Identify contradictions and missing information using rule-based and ML models.
4. **Source Recommendation**: When inconsistencies are found, suggest other articles or sources that cover those gaps, and summarize them.

