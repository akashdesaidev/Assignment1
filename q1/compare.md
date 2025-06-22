# 🔍 Tokenization Analysis Report
 
 ## ✉️ Input Sentence:
 > "The cat sat on the mat because it was tired."
 
 ---
 
 ## 1. *Byte Pair Encoding (BPE – GPT-2 Style)*
 
 - *Tokens*:  
   ['The', 'Ġcat', 'Ġsat', 'Ġon', 'Ġthe', 'Ġmat', 'Ġbecause', 'Ġit', 'Ġwas', 'Ġtired', '.']  
 - *Token IDs*:  
   [464, 3797, 3332, 319, 262, 2603, 780, 340, 373, 10032, 13]  
 - *Token Count*: 11
 
 ---
 
 ## 2. *WordPiece (Used by BERT Models)*
 
 - *Tokens*:  
   ['the', 'cat', 'sat', 'on', 'the', 'mat', 'because', 'it', 'was', 'tired', '.']  
 - *Token IDs*:  
   [1996, 4937, 2938, 2006, 1996, 13523, 2138, 2009, 2001, 5458, 1012]  
 - *Token Count*: 11
 
 ---
 
 ## 3. *SentencePiece (T5 Tokenizer)*
 
 - *Tokens*:  
   ['▁The', '▁cat', '▁', 's', 'at', '▁on', '▁the', '▁mat', '▁because', '▁it', '▁was', '▁tired', '.']  
 - *Token IDs*:  
   [37, 1712, 3, 7, 144, 30, 8, 6928, 250, 34, 47, 7718, 5]  
 - *Token Count*: 13
 
 ---
 
 ## ⚙️ Why the Tokenizations Vary
 
 Each tokenization method follows its own rules:
 
 - *BPE (Byte Pair Encoding)*: Builds words by merging common subword units (e.g., "ti" + "red" → "tired").
 - *WordPiece*: Uses prefix markers (##) to denote subwords that continue a word.
 - *SentencePiece*: Treats whitespace as a token (▁), allowing more flexible segmentation.
 
 Tokenization differences arise due to the tokenizer's internal vocabulary and segmentation strategy.
 
 ---
 
 ## 🧠 BERT-Style Masked Word Predictions
 
 ### 🔸 Original Prompt:
 > "The cat sat on the *[MASK]* because it was *[MASK]*."
 
 ### 🔹 First Mask Prediction ([MASK] → "the _")
 - *floor* (probability: 0.2534)  
 - *couch* (0.0875)  
 - *bed* (0.0874)
 
 ### 🔹 Second Mask Prediction (was ___)
 - *cold* (0.0537)  
 - *hungry* (0.0453)  
 - *warm* (0.0316)
 
 ---
 
 ## 📌 Interpretation
 
 The BERT model demonstrates contextual understanding:
 
 - For "sat on the ___", it suggests common resting places: *floor, **bed, **couch*.
 - For "because it was ___", it selects logical states: *cold, **hungry, **warm*.
 
 These predictions reflect real-world associations learned from large-scale text datasets such as Wikipedia and books.