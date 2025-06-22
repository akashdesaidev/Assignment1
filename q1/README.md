# Q1: Tokenization Analysis

This directory contains a comprehensive analysis of different tokenization methods used in modern NLP models.

## 📁 Files

- `tokenise.py` - Python script that demonstrates and compares different tokenization methods
- `compare.md` - Detailed analysis report with results and interpretations

## 🎯 Objective

The project analyzes how different tokenization algorithms process the same input sentence:
> "The cat sat on the mat because it was tired."

## 🔧 Tokenization Methods Compared

1. **Byte Pair Encoding (BPE)** - Used by GPT-2
2. **WordPiece** - Used by BERT models  
3. **SentencePiece** - Used by T5 models

## 🧠 Features

- **Tokenization Comparison**: Shows how each method breaks down the input sentence
- **Token ID Mapping**: Displays the numerical representation of tokens
- **Token Count Analysis**: Compares the efficiency of different tokenizers
- **BERT Masked Language Modeling**: Demonstrates contextual word prediction

## 🚀 Usage

### Prerequisites

Install the required dependencies:

```bash
pip install transformers torch sentencepiece
```

### Running the Analysis

```bash
python tokenise.py
```

This will output:
- Tokenization results for all three methods
- Token IDs and counts
- BERT masked word predictions

## 📊 Key Findings

- **BPE (GPT-2)**: 11 tokens with space markers (Ġ)
- **WordPiece (BERT)**: 11 tokens with clean word boundaries
- **SentencePiece (T5)**: 13 tokens with whitespace tokens (▁)

## 🔮 BERT Predictions

The script demonstrates BERT's ability to predict masked words:
- First [MASK]: Predicts physical locations (floor, couch, bed)
- Second [MASK]: Predicts emotional/physical states (cold, hungry, warm)

## 📝 Detailed Analysis

For a comprehensive breakdown of the results and interpretations, see `compare.md`.

## 🎓 Learning Outcomes

This analysis demonstrates:
- How tokenization affects model input processing
- The trade-offs between different tokenization strategies
- Contextual understanding in transformer models
- The importance of vocabulary design in NLP models 