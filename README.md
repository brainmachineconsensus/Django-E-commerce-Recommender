# Django E-commerce Recommender

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg) ![Django](https://img.shields.io/badge/django-4.0%2B-green.svg) ![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0%2B-orange.svg) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📖 Overview

This repository provides a **recommendation system** designed for Django-based e-commerce applications. It combines multiple recommendation strategies to enhance user experience by suggesting relevant products. The system is built as a modular component that can be integrated into existing Django projects.

### Key Features
- **Content-based filtering**: Recommends products similar to a given product based on category and description, using `TfidfVectorizer` and cosine similarity from scikit-learn.
- **Popularity-based recommendations**: Suggests the most popular products based on total sales volume.
- **City-based recommendations**: Recommends products popular in the user's city, leveraging order history.
- **Hybrid recommendations**: Combines content-based, popularity-based, and city-based methods to provide personalized and diverse suggestions.
- Robust error handling and logging for debugging and monitoring.
- Designed to work with Django ORM for seamless integration with `Product` and `Customer` models.

This is an example implementation for educational purposes, but it can be extended for production use with optimizations like caching or batch processing.

##  Getting Started

### Prerequisites
- Python 3.8 or higher
- Django 4.0 or higher
- scikit-learn 1.0 or higher
- A Django project with `Product` and `Customer` models (or equivalent) with the following fields:
  - `Product`: `category` (ForeignKey to a Category model), `description` (TextField), `name` (CharField)
  - `Customer`: `city` (CharField), `user` (ForeignKey to Django's User model)
  - Related models: `OrderPlaced` with `quantity` and links to `Product` and `Customer`

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/brainmachineconsensus/Django-E-commerce-Recommender.git
   cd django-ecommerce-recommender
   ```

2. **Install dependencies**:
   Create a virtual environment and install the required packages:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install scikit-learn django

   ```

3. **Integrate into your Django project**:
   - Copy `recommender.py` into your Django app (e.g., `your_app/recommender.py`).
   - Ensure your Django models match the expected structure (or update the code to fit your models).
   - Configure logging in your Django settings if needed (e.g., add a logger for `__name__`).

4. **Set up your Django project**:
   - Apply migrations: `python manage.py migrate`
   - Populate your database with sample `Product` and `Customer` data.

### Usage

1. **Initialize the recommender**:
   In your Django views or scripts, import and instantiate the `Recommender` class:
   ```python
   from your_app.recommender import Recommender
   recommender = Recommender()
   ```

2. **Generate recommendations**:
   Use the following methods to get recommendations:
   - **Content-based**:
     ```python
     recommendations = recommender.get_content_based_recommendations(product_id=1, num_recommendations=5)
     ```
   - **Popularity-based**:
     ```python
     recommendations = recommender.get_popularity_based_recommendations(num_recommendations=5)
     ```
   - **City-based**:
     ```python
     recommendations = recommender.get_city_based_recommendations(user=request.user, num_recommendations=5)
     ```
   - **Hybrid**:
     ```python
     recommendations = recommender.get_hybrid_recommendations(user=request.user, product_id=1, num_recommendations=5)
     ```

3. **Render in templates**:
   Pass the recommendations to your templates and display them:
   ```python
   # views.py
   def product_detail(request, product_id):
       recommendations = recommender.get_hybrid_recommendations(request.user, product_id)
       return render(request, 'product_detail.html', {'recommendations': recommendations})
   ```

## 📂 Project Structure

```
django-ecommerce-recommender/
├── recommender.py          # Core recommendation logic
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── LICENSE                # MIT License file
```

## 🛠️ Customization

- **Model adaptation**: Modify `recommender.py` to match your `Product` and `Customer` model fields if they differ (e.g., change `category.name` or `orderplaced` references).
- **Language support**: Adjust the `TfidfVectorizer` in `recommender.py` to support non-English languages by changing `stop_words='english'` to the appropriate language or a custom stop words list.
- **Performance optimization**:
  - Cache the `product_matrix` using Redis or Django's caching framework to avoid recomputing it frequently.
  - Precompute recommendations for popular products or cities in a background task (e.g., using Celery).
- **Additional features**:
  - Add user purchase history-based recommendations using collaborative filtering.
  - Incorporate product ratings or reviews into the recommendation logic.

## ⚠️ Notes

- The system assumes a populated database with sufficient product and order data for meaningful recommendations.
- Logging is configured to use Python's `logging` module. Ensure your Django project has a logging configuration to capture logs (e.g., in `settings.py`).
- This is a simplified example. For production, consider:
  - Adding unit tests (e.g., using Django's `TestCase`).
  - Implementing caching for the `product_matrix`.
  - Handling large datasets with batch processing or sparse matrices.

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a pull request.

Please include tests and documentation for new features.

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [Django](https://www.djangoproject.com/) and [scikit-learn](https://scikit-learn.org/).
- Inspired by common e-commerce recommendation patterns.

---

⭐ **Star this repository** if you find it useful! Feel free to open issues for questions or suggestions.
