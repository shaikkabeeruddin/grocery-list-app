# 🚀 Quick Start Guide

## ⚡ 5-Minute Setup

### **Step 1: Files**
```bash
# Copy these files to your project:
- app-final.py → app.py
- home-complete.html → templates/home.html
- (keep login.html, signup.html, forgot.html as is)
```

### **Step 2: Delete Old Data**
```bash
# Remove old database
del app.db
```

### **Step 3: Run**
```bash
python app.py
```

### **Step 4: Access**
```
http://localhost:5000
```

---

## 👤 Create Test Accounts

### **Account 1 (Sender)**
- Username: `alice`
- Email: `alice@test.com`
- Password: `123456`

### **Account 2 (Receiver)**
- Username: `bob`
- Email: `bob@test.com`
- Password: `123456`

---

## 📌 Testing Workflow (5 Minutes)

### **Step 1: Alice Creates List (2 min)**
1. Login as `alice`
2. Click "+ Create New List"
3. Title: `Weekly Groceries`
4. Select items:
   - Apple (1 kg)
   - Rice (5 kg)
   - Milk (1 lt)
   - Bread (2 pc)
5. Receiver: `bob`
6. Click "📤 Send List"

### **Step 2: Bob Receives & Completes (2 min)**
1. Login as `bob`
2. Click "Received" tab
3. Click "Weekly Groceries" card
4. Check items:
   - ✅ Apple (add price: 50)
   - ✅ Rice (add price: 200)
   - ❌ Milk (leave unchecked)
   - ❌ Bread (leave unchecked)
5. Click "✅ Mark as Done"
6. See success message

### **Step 3: Alice Views Results (1 min)**
1. Back to Alice account
2. Click "Sent Lists" tab
3. Click "Weekly Groceries" (now shows "Done")
4. See:
   - ✅ Collected: Apple (₹50), Rice (₹200)
   - ❌ Not Available: Milk, Bread

---

## 🎯 Key Features at a Glance

| Feature | Where | How |
|---------|-------|-----|
| **Create List** | Dashboard → "+ Create New List" | Select items, set qty, send |
| **View Sent Lists** | Dashboard → "Sent Lists" tab | Click to see results |
| **View Received Lists** | Dashboard → "Received" tab | Click to checkout |
| **Checkout** | Received list detail | Check items, add prices |
| **Mark Done** | Receiver checkout view | "✅ Mark as Done" button |
| **CSV Export** | Auto-generated | Saved to `groceries_data/` |
| **Price Tracking** | Receiver checkout | Optional price per item |

---

## 🏗️ File Structure

```
your-project/
├── app.py                    ← Backend Flask app
├── app.db                    ← SQLite database (auto-created)
├── groceries_data/           ← CSV exports (auto-created)
│   └── list_5_bob.csv
├── templates/
│   ├── home.html             ← Main dashboard
│   ├── login.html            ← Login page
│   ├── signup.html           ← Registration
│   └── forgot.html           ← Password reset
└── static/
    └── css/
        ├── style.css
        └── demo.css
```

---

## 📊 Data Flow Diagram

```
SENDER                           RECEIVER
├─ Login ──────────────────────► Logged In
├─ Create List
│  ├─ Select items
│  ├─ Set quantities
│  └─ Send to Receiver
│       └────────────────────────► List Received
│                                 ├─ View items (read-only)
│                                 ├─ Check items ✅
│                                 ├─ Add prices 💰
│                                 └─ Mark as Done ✓
│                                      └────────────────────────┐
│◄─────────────────────────── CSV Generated ──────────────────┘
├─ View Results
│  ├─ ✅ Collected items
│  ├─ ❌ Not available items
│  └─ Prices from receiver
└─ Done!
```

---

## 🔄 List Status Timeline

```
SENDER Creates          RECEIVER Works       RECEIVER Submits
━━━━━━━━━━━━━━━━━      ━━━━━━━━━━━━━━━━     ━━━━━━━━━━━━━━
     │                       │                    │
     ▼                       ▼                    ▼
  Pending            Checks items           Mark as Done
  (Draft)           Adds prices               │
     │              (15-30 min)                ▼
     │                   │                  Status: Done
     └───────────────────┴───────────────────────┘
                    CSV Generated
                  (groceries_data/)
```

---

## 🎨 UI Overview

### **Dashboard (Main Page)**
```
┌────────────────────────────────────┐
│ 🛒 Grocery Lists          [Logout] │
├────────────────────────────────────┤
│ Welcome, alice!                    │
│ [+ Create New List]                │
│                                    │
│ [Sent] [Received] [Drafts]        │
│                                    │
│ ┌────────────────────────────────┐ │
│ │ Weekly Groceries        [✓]    │ │
│ │ Status: Pending                │ │
│ │ 4 items                        │ │
│ └────────────────────────────────┘ │
│                                    │
│ ┌────────────────────────────────┐ │
│ │ Office Supplies        [Done]  │ │
│ │ Status: Done                   │ │
│ │ 8 items                        │ │
│ └────────────────────────────────┘ │
└────────────────────────────────────┘
```

### **Create List View**
```
┌─────────────────────────────────────┐
│ [← Back]                            │
│                                     │
│ Create Grocery List                 │
│ ┌─────────────────────────────────┐ │
│ │ List Title: [Weekly Groceries] │ │
│ │ From: alice                    │ │
│ │ To: [bob ▼]                    │ │
│ └─────────────────────────────────┘ │
│                                     │
│ 📦 Select Items from Catalog       │
│ ┌──────────┬──────────┬──────────┐ │
│ │Vegetables│ Fruits  │  Dairy   │ │
│ │ Tomato  │ Apple   │ Milk     │ │
│ │ Potato  │ Banana  │ Cheese   │ │
│ │ Onion   │ Mango   │ Eggs     │ │
│ └──────────┴──────────┴──────────┘ │
│                                     │
│ 📋 Selected Items    │  ✓ Summary  │
│ ┌────────────────┐  │ ┌─────────┐ │
│ │ Apple, 1 kg ✕ │  │ │ Apple   │ │
│ │ Rice, 5 kg  ✕ │  │ │ Rice    │ │
│ │ Milk, 1 lt  ✕ │  │ │ Milk    │ │
│ └────────────────┘  │ │ Bread   │ │
│                     │ │         │ │
│                     │ │[💾][📤] │ │
│                     │ └─────────┘ │
│                     │             │
│ 🔍 Add Custom Item  │             │
│ [Add item here] ↵   │             │
└─────────────────────────────────────┘
```

### **Receiver Checkout View**
```
┌───────────────────────────────┐
│ [← Back]                      │
│                               │
│ Weekly Groceries              │
│ Status: [Pending]             │
│                               │
│ ✅ COLLECTED ITEMS            │
│ ┌─────────────────────────┐   │
│ │ ☑ Apple, 1 kg   ₹[50]  │   │
│ │ ☑ Rice, 5 kg    ₹[200] │   │
│ └─────────────────────────┘   │
│                               │
│ ❌ NOT AVAILABLE              │
│ ┌─────────────────────────┐   │
│ │ ☐ Milk, 1 lt    ₹[ ]   │   │
│ │ ☐ Bread, 2 pc   ₹[ ]   │   │
│ └─────────────────────────┘   │
│                               │
│    [✅ Mark as Done]          │
└───────────────────────────────┘
```

### **Sender Results View**
```
┌───────────────────────────────┐
│ [← Back]                      │
│                               │
│ Weekly Groceries              │
│ Status: [Completed]           │
│                               │
│ ✅ COLLECTED BY RECEIVER      │
│ ┌─────────────────────────┐   │
│ │ ✅ Apple, 1 kg   ₹50   │   │
│ │ ✅ Rice, 5 kg    ₹200  │   │
│ └─────────────────────────┘   │
│                               │
│ ❌ NOT AVAILABLE              │
│ ┌─────────────────────────┐   │
│ │ ❌ Milk, 1 lt          │   │
│ │ ❌ Bread, 2 pc         │   │
│ └─────────────────────────┘   │
│                               │
│ ✓ List completed. Receiver   │
│   has submitted their response│
└───────────────────────────────┘
```

---

## 💾 CSV File Example

**File:** `groceries_data/list_5_bob.csv`

```
Item Name,Quantity,Unit,Price,Status,Receiver,Date
Apple,1,kg,50,Collected,bob,2026-01-26 17:21:00
Rice,5,kg,200,Collected,bob,2026-01-26 17:21:00
Milk,1,lt,,Not Available,bob,2026-01-26 17:21:00
Bread,2,pc,,Not Available,bob,2026-01-26 17:21:00
```

### **Open in Excel/Google Sheets**
1. Right-click `list_5_bob.csv`
2. Open with → Excel/Sheets
3. Create charts, pivot tables, analysis

---

## 🎓 Learning Resources

### **JavaScript Functions (Key)**
- `openListDetail()` - Load list detail view
- `renderReceiverCheckoutView()` - Show checkout UI
- `updateReceiverItem()` - Track checked items & prices
- `markListDone()` - Submit & save to CSV
- `renderSenderCompletedView()` - Show results

### **Flask Routes (Key)**
- `POST /api/groceries` - Create list
- `GET /api/groceries/<type>` - Get lists
- `POST /api/groceries/send/<id>` - Send list
- `POST /api/groceries/mark-done/<id>` - Complete & export

---

## ❓ Common Questions

**Q: Can I edit a list after sending?**  
A: No, lists are locked once receiver starts working on them.

**Q: Are prices required?**  
A: No, prices are optional for each item.

**Q: Where are CSV files saved?**  
A: In `groceries_data/` folder in your project root.

**Q: Can receiver add items?**  
A: No, only sender creates items. Receiver only checks availability.

**Q: Can I send to multiple people?**  
A: Currently no, but planned for future versions.

**Q: How long are lists kept?**  
A: Until deleted manually. CSV files are permanent.

---

## 🎉 You're All Set!

**Everything is ready to use.** Just:
1. Copy the files
2. Run `python app.py`
3. Create accounts
4. Start using! 

**Happy Shopping! 🛒**

