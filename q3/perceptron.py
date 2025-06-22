import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read the dataset
dataset = pd.read_csv('fruits.csv')
features = dataset[['length_cm', 'weight_g', 'yellow_score']].values
targets = dataset['label'].values.reshape(-1, 1)

# Feature scaling (standardization)
features = (features - np.mean(features, axis=0)) / np.std(features, axis=0)

# Weight and bias initialization
np.random.seed(42)
theta = np.random.randn(features.shape[1], 1)
intercept = 0

# Sigmoid activation function
def sigmoid_fn(x):
    return 1 / (1 + np.exp(-x))

# Binary cross-entropy loss
def compute_loss(actual, predicted):
    samples = actual.shape[0]
    return -np.sum(actual * np.log(predicted) + (1 - actual) * np.log(1 - predicted)) / samples

# Logistic regression forward step
def forward_pass(input_data, theta, intercept):
    linear_output = np.dot(input_data, theta) + intercept
    return sigmoid_fn(linear_output)

# Hyperparameters
lr = 0.1
max_epochs = 500
loss_track = []
acc_track = []

# Training process
for epoch in range(max_epochs):
    pred = forward_pass(features, theta, intercept)

    # Compute current loss
    loss_val = compute_loss(targets, pred)
    loss_track.append(loss_val)

    # Compute accuracy
    classified = (pred >= 0.5).astype(int)
    acc = np.mean(classified == targets)
    acc_track.append(acc)

    # Gradients
    m = targets.shape[0]
    error = pred - targets
    grad_theta = np.dot(features.T, error) / m
    grad_bias = np.sum(error) / m

    # Update step
    theta -= lr * grad_theta
    intercept -= lr * grad_bias

    # Early stopping condition
    if loss_val < 0.05:
        print(f"Training stopped early at epoch {epoch}")
        break

    if epoch % 50 == 0:
        print(f"Epoch {epoch} | Loss: {loss_val:.4f} | Accuracy: {acc:.4f}")

# Final results
final_pred = forward_pass(features, theta, intercept)
final_classified = (final_pred >= 0.5).astype(int)
final_accuracy = np.mean(final_classified == targets)

print(f"\nFinal Results:")
print(f"Final Accuracy: {final_accuracy:.4f}")
print(f"Final Loss: {loss_track[-1]:.4f}")
print(f"Initial vs Final Loss: {loss_track[0]:.4f} -> {loss_track[-1]:.4f}")

# Visualizations
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(loss_track, label='Loss')
plt.title("Loss Curve")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(acc_track, label='Accuracy', color='green')
plt.title("Accuracy Curve")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.grid(True)

plt.tight_layout()
plt.show()