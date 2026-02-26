# Budgetly - Personal Budget Manager

## Sample Data Created Successfully! 🎉

### Test User Credentials
- **Username**: `testuser`
- **Password**: `testpass123`
- **Email**: `test@budgetly.com`

### Sample Budget Data
- **Monthly Income**: Nrs5,000.00
- **Savings Goal**: Nrs1,000.00 (20% of income)
- **Total Expenses**: 27 expenses across all categories
- **Total Spent**: Nrs2,538.86
- **Remaining Budget**: Nrs1,461.14

## How to Start the Server

1. Open PowerShell/Command Prompt
2. Navigate to the project directory:
   ```
   cd "C:\Users\ACER\OneDrive\Desktop\D.djan\budgetly"
   ```
3. Activate virtual environment:
   ```
   ..\budgetly_env\Scripts\Activate.ps1
   ```
4. Start the server:
   ```
   python manage.py runserver
   ```
5. Open your browser and go to: `http://127.0.0.1:8000/`

## Features to Test

### 🏠 **Home Page** (`/`)
- Landing page with features overview
- Call-to-action buttons for registration/login

### 🔐 **Authentication** (`/accounts/`)
- **Register**: Create new account (`/accounts/register/`)
- **Login**: Use testuser credentials (`/accounts/login/`)
- **Logout**: Click username dropdown → Logout (now uses POST form)

### 💰 **Budget Management** (`/budget/setup/`)
- View current budget: Nrs5,000 income, Nrs1,000 savings goal
- Edit monthly income and savings goals
- See budget summary with percentages

### 💸 **Expense Tracking** (`/expenses/`)
- **View Expenses**: See 27 sample expenses across categories
- **Add Expense**: Create new expenses with category selection
- **Categories Available**:
  - Food & Dining (groceries, restaurants, coffee)
  - Transportation (gas, uber, parking, bus pass)
  - Entertainment (movies, streaming, concerts, games)
  - Utilities (electric, internet, water bills)
  - Healthcare (pharmacy, doctor visits, gym)
  - Shopping (clothing, online purchases, books)
  - Housing (rent, home supplies)
  - Education (courses, books)
  - Personal Projects (custom category)

###  **Reports & Dashboard** (`/reports/`)
- **Budget Overview Cards**: Income, Savings Goal, Total Spent
- **Pie Chart**: Spending breakdown by category (powered by Chart.js)
- **Recent Expenses List**: Latest transactions
- **Quick Actions**: Navigate to key features
- **Savings Analysis**: Track progress toward financial goals

### 👨‍💼 **Admin Panel** (`/admin/`)
- **Admin User**: username `admin`, password set during setup
- Manage users, budgets, expenses, and categories
- Filter and search functionality

## Sample Data Details

### Expense Categories with Sample Data:
1. **Food & Dining** (Nrs195.74): Groceries, restaurants, coffee shops
2. **Transportation** (Nrs173.50): Gas, ride-sharing, parking, transit
3. **Entertainment** (Nrs178.98): Movies, streaming, concerts, games  
4. **Utilities** (Nrs245.94): Electric, internet, water bills
5. **Healthcare** (Nrs110.98): Pharmacy, doctor visits, gym membership
6. **Shopping** (Nrs164.48): Clothing, online purchases, books
7. **Housing** (Nrs1,265.75): Rent, home improvement supplies
8. **Education** (Nrs174.50): Online courses, educational books
9. **Personal Projects** (Nrs29.99): Custom category example

### Time Range:
- Expenses spread over the last 30 days
- Realistic amounts and descriptions
- Mix of daily, weekly, and monthly expenses

## Testing Checklist 

1. **Authentication Flow**:
   - [ ] Register new user
   - [ ] Login with testuser
   - [ ] Logout (should redirect to home)

2. **Budget Features**:
   - [ ] View current budget setup
   - [ ] Edit income and savings goal
   - [ ] See budget calculations

3. **Expense Management**:
   - [ ] View expense list with sample data
   - [ ] Add new expense with category selection
   - [ ] See expenses by different categories

4. **Reports & Analytics**:
   - [ ] View dashboard with budget overview
   - [ ] See pie chart visualization
   - [ ] Check recent expenses list
   - [ ] Verify quick actions work

5. **Navigation & UI**:
   - [ ] Test responsive navbar
   - [ ] Check all menu links work
   - [ ] Verify theme color (#9381FF) throughout
   - [ ] Test Bootstrap styling

6. **Error Handling**:
   - [ ] Try invalid form submissions
   - [ ] Check form validation messages
   - [ ] Test required field validation

## Architecture Highlights

- **Pluggable Apps**: Each feature is a separate Django app
- **MVT Pattern**: Models, Views, Templates properly separated
- **Bootstrap 5**: Responsive design with custom theme
- **Chart.js**: Interactive data visualizations
- **Security**: CSRF protection, POST-based logout
- **Reusable**: Apps can be used in other Django projects

Enjoy testing your Budgetly application! 
