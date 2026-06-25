#!/bin/bash

echo "========================================="
echo "🚀 Starting Jenkins Build Process"
echo "========================================="
echo "Build Number: $BUILD_NUMBER"
echo "Branch: $GIT_BRANCH"
echo "Commit: $GIT_COMMIT"
echo "Workspace: $WORKSPACE"
echo "========================================="

# Устанавливаем Python зависимости
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Проверяем синтаксис с flake8
echo "🔍 Running flake8 linter..."
flake8 app.py test_app.py --max-line-length=120 --ignore=E402,F841

if [ $? -ne 0 ]; then
    echo "❌ Linter found issues!"
    exit 1
fi
echo "✅ Linter passed!"

# Запускаем тесты
echo "🧪 Running unit tests..."
python3 -m pytest test_app.py -v

if [ $? -ne 0 ]; then
    echo "❌ Tests failed!"
    exit 1
fi
echo "✅ All tests passed!"

# Создаем артефакт сборки
echo "📦 Creating build artifacts..."
echo "Build successful!" > build-info.txt
echo "Build number: $BUILD_NUMBER" >> build-info.txt
echo "Build time: $(date)" >> build-info.txt

# Упаковываем приложение (опционально)
zip -r app-$BUILD_NUMBER.zip app.py requirements.txt

echo "========================================="
echo "✅ Build completed successfully!"
echo "========================================="