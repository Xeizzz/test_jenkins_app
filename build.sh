#!/bin/bash

echo "========================================="
echo "🚀 Starting Jenkins Build Process"
echo "========================================="
echo "Build Number: $BUILD_NUMBER"
echo "Branch: $GIT_BRANCH"
echo "Commit: $GIT_COMMIT"
echo "Workspace: $WORKSPACE"
echo "========================================="

# Создаем виртуальное окружение
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv --system-site-packages

# Активируем виртуальное окружение
source venv/bin/activate

# Обновляем pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Устанавливаем зависимости
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Проверяем flake8
echo "🔍 Running flake8 linter..."
flake8 app.py test_app.py --max-line-length=120 --ignore=E402,F841

if [ $? -ne 0 ]; then
    echo "❌ Linter found issues!"
    deactivate
    exit 1
fi
echo "✅ Linter passed!"

# Запускаем тесты
echo "🧪 Running unit tests..."
pytest test_app.py -v

if [ $? -ne 0 ]; then
    echo "❌ Tests failed!"
    deactivate
    exit 1
fi
echo "✅ All tests passed!"

# Создаем артефакт сборки
echo "📦 Creating build artifacts..."
echo "Build successful!" > build-info.txt
echo "Build number: $BUILD_NUMBER" >> build-info.txt
echo "Build time: $(date)" >> build-info.txt
echo "Python version: $(python --version)" >> build-info.txt

# Упаковываем приложение
zip -r app-$BUILD_NUMBER.zip app.py requirements.txt build-info.txt

# Деактивируем виртуальное окружение
deactivate

echo "========================================="
echo "✅ Build completed successfully!"
echo "========================================="
