from transformers import AutoTokenizer, pipeline
import sentencepiece as spm  # Required for SentencePiece models

# Input sentence to analyze
text_input = "The cat sat on the mat because it was tired."

# Load tokenizer models
tokenizer_gpt2 = AutoTokenizer.from_pretrained("gpt2")  # Byte-Pair Encoding (BPE)
tokenizer_bert = AutoTokenizer.from_pretrained("bert-base-uncased")  # WordPiece
tokenizer_t5 = AutoTokenizer.from_pretrained("google-t5/t5-small")  # SentencePiece

# Function to display tokenization details
def show_tokenization(method_label, tokenizer_instance):
    print(f"\n🧠 {method_label} Tokenizer")
    split_tokens = tokenizer_instance.tokenize(text_input)
    token_ids = tokenizer_instance.convert_tokens_to_ids(split_tokens)
    print("Tokens      :", split_tokens)
    print("Token IDs   :", token_ids)
    print("Token Count :", len(split_tokens))

# Compare the tokenization schemes
show_tokenization("BPE (GPT-2)", tokenizer_gpt2)
show_tokenization("WordPiece (BERT)", tokenizer_bert)
show_tokenization("SentencePiece (T5)", tokenizer_t5)

# --- Predict Masked Words Using BERT ---
print("\n🔮 Predicting Masked Words with BERT")

# Prepare pipeline for masked word prediction
mask_predictor = pipeline("fill-mask", model="bert-base-uncased")

# Sentence with placeholders
masked_text = "The cat sat on the [MASK] because it was [MASK]."

# Run the model
prediction_results = mask_predictor(masked_text)

# Debug output (optional)
print("\n📦 Raw Prediction Output:")
print(prediction_results)

# Display top predictions for first [MASK]
print("\n🔍 Top Predictions for First [MASK]:")
top_first = prediction_results[0]
for index, guess in enumerate(top_first[:3]):
    print(f"{index + 1}. {guess['sequence']} (confidence: {guess['score']:.4f})")

# Display top predictions for second [MASK]
print("\n🔍 Top Predictions for Second [MASK]:")
top_second = prediction_results[1]
for index, guess in enumerate(top_second[:3]):
    print(f"{index + 1}. {guess['sequence']} (confidence: {guess['score']:.4f})")