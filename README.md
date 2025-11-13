# 🎭 Artist Network Clustering & Community Detection  
*Phân cụm mạng lưới nghệ sĩ gameshow & phát hiện nhóm hợp tác thường xuyên*

![Stars](https://img.shields.io/github/stars/maithanhphuc2004/Artist-Network-Clustering?style=flat-square)
![Forks](https://img.shields.io/github/forks/maithanhphuc2004/Artist-Network-Clustering?style=flat-square)
![Issues](https://img.shields.io/github/issues/maithanhphuc2004/Artist-Network-Clustering?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/maithanhphuc2004/Artist-Network-Clustering?color=green&style=flat-square)

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)

---

## 📌 Overview *(Tổng quan)*  
This project constructs and analyzes a large-scale **Vietnamese artist collaboration network** based on gameshow co-appearances.  
The dataset was collected automatically using Selenium from Wikipedia, then processed to form a graph containing:

- **675 artists (nodes)**  
- **55,262 co-appearance relationships (edges)**  

The goal of the study is to:

- Identify influential artists  
- Detect collaboration communities  
- Understand structural patterns in entertainment networks  
- Provide insights for recommendation systems (partner suggestion, show casting)

This study demonstrates how **Social Network Analysis (SNA)** combined with **modern clustering algorithms** can reveal meaningful artist groups and cooperation behavior in the entertainment industry of Vietnam.

---

## 🧠 Centrality Metrics *(Chỉ số trung tâm)*  
To analyze influence and importance of artists, the project computes:

| Metric | Meaning | Insight |
|--------|---------|---------|
| **Degree Centrality** | Number of direct connections | Measures popularity |
| **Betweenness Centrality** | How often a node is a bridge | Detects "connector" artists |
| **Closeness Centrality** | Average distance to all others | Communication efficiency |
| **PageRank** | Global relevance score | Identifies influential artists |

These metrics allow us to detect central figures such as:  
✨ **Kim Tử Long**, **Hoài Linh**, **Hòa Minzy**, …  
who act as "hubs" in the artist gameshow network.

---

## 🧩 Community Detection Algorithms  
The study applies four modern, widely used clustering algorithms:

### 🔥 **Bảng so sánh thuật toán** (đẹp – trình bày rõ)

| Algorithm | Description | Strengths | Weaknesses | Modularity (Higher = Better) |
|-----------|-------------|-----------|------------|-------------------------------|
| **Louvain** | Hierarchical modularity optimization | Fast, scalable | May produce disconnected communities | 0.3561 |
| **Leiden** | Improved Louvain ensuring well-connected communities | **Best modularity**, stable | Slightly more complex | **0.3784** |
| **Spectral Clustering** | Uses Laplacian eigenvectors | Solid theoretical foundation | Requires number of clusters K | 0.3310 |
| **Gaussian Mixture Model (GMM)** | Probabilistic soft clustering | Detects overlapping communities | Sensitive to initialization | 0.2985 |

🎯 **Key finding:**  
👉 **Leiden is the best-performing algorithm**, producing clearer and more meaningful artist communities.

---

## 🎭 Collaboration Groups *(Nhóm nghệ sĩ hợp tác thường xuyên)*  
From clustering results, several strong and stable artist communities emerge.  
Typical examples:

- **Group 1:** Hòa Minzy – Hari Won – Trấn Thành – Trường Giang  
- **Group 2:** Hồ Ngọc Hà – Thanh Hằng – Minh Hằng  
- **Group 3:** Đại Nghĩa – Ngô Kiến Huy – Khả Như  

These communities represent real-world collaboration patterns seen across Vietnamese reality shows and TV entertainment programs.

---

## 🎯 Key Contributions *(Đóng góp chính của nghiên cứu)*  
This project provides several practical and methodological contributions:

### ✔ 1. Built a scalable, high-resolution artist social network  
A reusable, expandable dataset useful for future entertainment analytics.

### ✔ 2. Compared four state-of-the-art community detection algorithms  
Provides empirical benchmarking on real entertainment data.

### ✔ 3. Identified meaningful collaboration structures  
Helps producers, casting teams, and researchers understand artist dynamics.

### ✔ 4. Supports potential real-world applications  
- Partner recommendation  
- Cast planning for gameshows  
- Trend detection in entertainment  
- Social influence analysis  

---

## 📁 Installation

```bash
pip install -r requirements.txt
python src/network/build_graph.py
python src/network/calculate_metrics.py
python src/clustering/run_clustering.py
python src/visualize/plot_network.py
```
##📚 Citation
Mai Thanh Phúc, Hoàng Thị Yến Nhi, Trần Trọng Thành, Lê Nhật Tùng.
Artist Network Clustering and Community Detection in Vietnamese Gameshows.
HUTECH University.

