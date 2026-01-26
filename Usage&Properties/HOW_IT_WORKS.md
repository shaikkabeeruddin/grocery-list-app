# 🛒 Groceries List Manager - Complete Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [User Roles](#user-roles)
3. [User Flow](#user-flow)
4. [Features](#features)
5. [Setup Instructions](#setup-instructions)
6. [API Endpoints](#api-endpoints)
7. [Data Models](#data-models)
8. [CSV Export](#csv-export)

---

## 📖 Overview

**Groceries List Manager** is a web application that allows users to:
- Create grocery shopping lists
- Send lists to other users (receivers)
- Receivers can mark items as collected/unavailable
- Add optional prices for each item
- Automatically generate CSV files for record-keeping
- Track what items were available vs. not available

**Tech Stack:**
- Backend: Flask (Python)
- Frontend: HTML + Vanilla JavaScript
- Database: SQLite
- Export: CSV

---

## 👥 User Roles

### **Sender**
- Creates grocery lists
- Selects items from catalog or adds custom items
- Sets quantities and units
- Sends lists to receivers
- Cannot edit lists once receiver starts working
- Views final results (collected vs. not available items)

### **Receiver**
- Receives shopping lists
- Cannot add/edit/delete items
- Checks items they have available ✅
- Leaves unchecked items they don't have ❌
- Optionally adds prices for cost tracking
- Clicks "Mark as Done" to submit response
- CSV automatically saved for record-keeping

---

## 🔄 User Flow

### **Complete Workflow**

```
┌─────────────────────────────────────────────────────────────┐
│                    SENDER WORKFLOW                          │
├─────────────────────────────────────────────────────────────┤
│ 1. Login                                                    │
│ 2. Click "+ Create New List"                               │
│ 3. Enter List Title (e.g., "Weekly Groceries")            │
│ 4. Browse Catalog & Select Items OR Add Custom Items      │
│ 5. Set Quantities & Units for each item                   │
│ 6. Select Receiver from dropdown                          │
│ 7. Click "📤 Send List"                                   │
│ 8. List is sent to receiver                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   RECEIVER WORKFLOW                         │
├─────────────────────────────────────────────────────────────┤
│ 1. Login                                                    │
│ 2. Click "Received" Tab                                   │
│ 3. Click on the list card to open                         │
│ 4. See two sections:                                      │
│    ✅ Checked Items (collected - green)                   │
│    ❌ Unchecked Items (not available - red)              │
│ 5. Check items you have ✅                                │
│ 6. Leave unchecked items you don't have ❌                │
│ 7. Optionally add prices for each item (₹)               │
│ 8. Click "✅ Mark as Done"                               │
│ 9. CSV file generated automatically                       │
│ 10. List marked as complete                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              SENDER VIEWS RESULTS WORKFLOW                 │
├─────────────────────────────────────────────────────────────┤
│ 1. Go to "Sent Lists" tab                                 │
│ 2. Click on list (now shows as "Done")                    │
│ 3. See two sections:                                      │
│    ✅ Items receiver collected (green)                    │
│    ❌ Items not available (red)                           │
│ 4. See prices entered by receiver                         │
│ 5. List is read-only (cannot edit anymore)               │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### **1. List Management**

#### **Create List**
- Browse 10 categories of pre-defined items
- Vegetables, Fruits, Grains, Spices, Dairy, Meat, Snacks, Beverages, Oils, Others
- Add custom items by typing and pressing Enter
- Adjust quantities (0.5 - unlimited)
- Select units: kg, gm, lt, ml, pc
- Save as draft or send immediately

#### **List Types**
- **Drafts:** Unsent lists, editable
- **Sent:** Lists sent to receivers, view results
- **Received:** Lists from other users, checkout interface

### **2. Receiver Checkout Interface**

#### **Visual Separation**
```
┌─────────────────────────────────────┐
│ 📦 List Title                       │
├─────────────────────────────────────┤
│ Status: [Pending/Done]              │
├─────────────────────────────────────┤
│                                     │
│ ✅ COLLECTED ITEMS (Green Section) │
│ ┌─────────────────────────────────┐ │
│ │ ☑ Apple, 1 kg      Price: ₹50  │ │
│ │ ☑ Rice, 5 kg       Price: ₹200 │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ❌ NOT AVAILABLE (Red Section)      │
│ ┌─────────────────────────────────┐ │
│ │ ☐ Milk, 1 lt       Price: —    │ │
│ │ ☐ Bread, 2 pc      Price: —    │ │
│ └─────────────────────────────────┘ │
│                                     │
│         [✅ Mark as Done]           │
└─────────────────────────────────────┘
```

#### **Checkbox Functionality**
- ✅ Check items you have available
- ❌ Leave unchecked items you don't have
- Items automatically reorganize into sections
- Prices are optional per item
- Disabled after marking as done

### **3. CSV Export**

#### **Automatic Generation**
- File saved to: `groceries_data/list_{id}_{username}.csv`
- Generated when receiver clicks "Mark as Done"
- Contains 7 columns:
  - Item Name
  - Quantity
  - Unit
  - Price (if entered)
  - Status (Collected/Not Available)
  - Receiver Name
  - Timestamp

#### **CSV Example**
```csv
Item Name,Quantity,Unit,Price,Status,Receiver,Date
Apple,1,kg,50,Collected,john,2026-01-26 17:21:00
Rice,5,kg,200,Collected,john,2026-01-26 17:21:00
Milk,1,lt,,Not Available,john,2026-01-26 17:21:00
Bread,2,pc,,Not Available,john,2026-01-26 17:21:00
```

### **4. Price Tracking**

- Receiver can add price per item (optional)
- Prices appear in CSV for future analysis
- Sender can see prices in results view
- Use for budget tracking, cost analysis, future reports

### **5. Status Management**

| Status | Description | Who Sets | Action |
|--------|-------------|----------|--------|
| Pending | List created, not yet submitted | System | Created |
| Done | Receiver submitted response | Receiver | Mark as Done |
| Collected | Item was available | Receiver | Check checkbox |
| Not Available | Item was not available | Receiver | Leave unchecked |

---

## 🚀 Setup Instructions

### **Prerequisites**
- Python 3.8+
- Flask
- SQLite (built-in)

### **Installation Steps**

1. **Create Project Folder**
```bash
mkdir groceries-app
cd groceries-app
```

2. **Create Folder Structure**
```bash
mkdir templates static/css
```

3. **Place Files**
- `app.py` → Root folder
- `home.html` → `templates/`
- `login.html` → `templates/`
- `signup.html` → `templates/`
- `forgot.html` → `templates/`
- `style.css` → `static/css/`
- `demo.css` → `static/css/`

4. **Install Flask**
```bash
pip install flask
```

5. **Run App**
```bash
python app.py
```

6. **Access**
```
http://localhost:5000
```

### **First Time Setup**
1. Navigate to http://localhost:5000
2. You'll be redirected to login (first time)
3. Click "Sign Up"
4. Create 2 test accounts:
   - Account 1: user1 / test@test.com / 123456
   - Account 2: user2 / test2@test.com / 123456
5. Start testing workflow

---

## 🔗 API Endpoints

### **Authentication**
```
POST /api/signup
POST /api/login
POST /api/logout
POST /api/forgot/request
POST /api/forgot/verify
POST /api/forgot/reset
```

### **Users**
```
GET /api/users
→ Returns all users except current user
→ Response: { ok: true, users: [{ id, username }, ...] }
```

### **Catalog**
```
GET /api/catalog
→ Returns pre-defined grocery items by category
→ Response: { ok: true, catalog: { "Vegetables": [...], ... } }
```

### **Grocery Lists**

#### **Get Lists**
```
GET /api/groceries/<list_type>
→ list_type: "sent", "received", or "drafts"
→ Response: { ok: true, lists: [...] }
```

#### **Get Single List**
```
GET /api/groceries/<list_id>
→ Response: { ok: true, list: { id, title, items, status, list_type } }
```

#### **Create List**
```
POST /api/groceries
Body: {
  "list_type": "drafts",
  "title": "Weekly Groceries",
  "items": [{ name, qty, unit }, ...],
  "status": "Pending"
}
→ Response: { ok: true }
```

#### **Delete List**
```
DELETE /api/groceries/<list_id>
→ Only for draft lists
→ Response: { ok: true, message: "List deleted." }
```

#### **Send List**
```
POST /api/groceries/send/<list_id>
Body: { "receiver_id": 2 }
→ Creates received list for receiver
→ Updates sender's list to "sent"
→ Response: { ok: true, message: "List sent successfully!" }
```

#### **Mark as Done** ⭐ **NEW**
```
POST /api/groceries/mark-done/<list_id>
Body: {
  "checked_items": [
    { "name": "Apple", "checked": true, "price": 50 },
    { "name": "Milk", "checked": false, "price": 0 }
  ]
}
→ Updates list status to "Done"
→ Generates CSV file
→ Response: { ok: true, message: "List marked as done! CSV saved." }
```

---

## 📊 Data Models

### **User Table**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

### **Grocery Lists Table**
```sql
CREATE TABLE grocery_lists (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    list_type TEXT NOT NULL,        -- "sent", "received", "drafts"
    title TEXT NOT NULL,
    items_json TEXT NOT NULL,       -- JSON array
    status TEXT NOT NULL,           -- "Pending", "Done"
    receiver_id INTEGER,            -- ID of receiver (for sent lists)
    created_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
```

### **Item Object (JSON)**
```json
{
    "id": 1234567890,
    "name": "Apple",
    "qty": 2,
    "unit": "kg",
    "price": 50,              // Added by receiver (optional)
    "checked": true           // Added by receiver
}
```

---

## 📁 CSV Export Details

### **File Location**
```
groceries_data/list_<list_id>_<username>.csv
```

**Example:** `groceries_data/list_5_user1.csv`

### **Column Structure**

| Column | Description | Example |
|--------|-------------|---------|
| Item Name | Name of grocery item | Apple |
| Quantity | Amount ordered | 2 |
| Unit | Unit of measurement | kg |
| Price | Price entered by receiver (optional) | 50 |
| Status | Collection status | Collected / Not Available |
| Receiver | Who submitted the list | john |
| Date | Timestamp of submission | 2026-01-26 17:21:00 |

### **Usage**
- Import into Excel/Google Sheets
- Create pivot tables for analytics
- Track cost over time
- Build shopping history reports
- Identify items frequently unavailable

---

## 🎨 UI Components

### **Dashboard**
- Header with user greeting
- 3 Tabs: Sent Lists | Received | Drafts
- Grid of list cards
- "+ Create New List" button

### **Create List View**
- List title input
- Sender name (read-only)
- Receiver dropdown
- Scrollable catalog (10 categories)
- Custom item search box
- Selected items list with qty/unit
- Summary box with action buttons

### **Receiver Checkout View**
- List title and status
- ✅ Collected Items section (green)
- ❌ Not Available section (red)
- Checkboxes for each item
- Price input fields
- "Mark as Done" button

### **Sender Results View**
- List title and "Completed" status
- ✅ Items collected by receiver (green)
- ❌ Items not available (red)
- Prices visible (if entered)
- Read-only (no editing)

---

## 🔐 Security Features

- Password hashing using werkzeug
- Session-based authentication
- CSRF protection ready
- Input validation on all endpoints
- User isolation (can only see own lists + received lists)

---

## 🚨 Troubleshooting

### **Lists not showing**
- Clear browser cache
- Logout and login again
- Check database exists: `app.db`

### **CSV not generated**
- Check `groceries_data/` folder exists
- Ensure write permissions on folder
- Check server logs for errors

### **Receiver can't see list**
- Sender must select receiver correctly
- Receiver must be already registered
- Check "Received" tab in receiver account

### **Prices not saving**
- Only receiver can add prices
- Prices only save when clicking "Mark as Done"
- Prices must be numeric

---

## 📈 Future Enhancements

- [ ] Real-time notifications
- [ ] Item availability percentage tracking
- [ ] Cost analytics dashboard
- [ ] Recurring lists
- [ ] Multiple receivers per list
- [ ] Item comments/notes
- [ ] Email integration
- [ ] Mobile app
- [ ] Barcode scanning
- [ ] Inventory management

---

## 📞 Support

For issues or questions:
1. Check this documentation
2. Review API endpoints
3. Check browser console for JavaScript errors
4. Check server logs for Flask errors

---

## 📝 License

This application is provided as-is for educational and personal use.

---

**Last Updated:** January 26, 2026  
**Version:** 1.0  
**Status:** Production Ready ✅
