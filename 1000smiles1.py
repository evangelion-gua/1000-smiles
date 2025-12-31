# python -m streamlit run C:\Users\s2chc\AppData\Local\Programs\Python\Python311\stream6.py
import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import uuid

# Set page configuration
st.set_page_config(page_title="Toy Donation Charity", page_icon="❤️", layout="wide")

# Initialize database
def init_database():
    conn = sqlite3.connect('charity_students.db')
    c = conn.cursor()
    
    # Create students table
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, 
                  age INTEGER,
                  year_of_birth INTEGER,
                  favourite_hobby TEXT,
                  favourite_colour TEXT,
                  school TEXT,
                  donation_count INTEGER,
                  member_grade TEXT,
                  registration_date TIMESTAMP)''')
    
    # Create photos table
    c.execute('''CREATE TABLE IF NOT EXISTS photos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id INTEGER,
                  photo_base64 TEXT,
                  message TEXT,
                  smile_rating INTEGER,
                  uploaded_date TIMESTAMP,
                  FOREIGN KEY(student_id) REFERENCES students(id))''')
    
    # Check if we have at least 50 records
    c.execute("SELECT COUNT(*) FROM students")
    count = c.fetchone()[0]
    
    if count < 50:
        # Generate Malaysian names
        malay_names = [
            "Ahmad", "Ali", "Aina", "Amir", "Aisyah", "Bakar", "Chong", "Fatimah", "Hassan", 
            "Ibrahim", "Jamal", "Kumar", "Lee", "Lim", "Mei", "Mohd", "Nurul", "Omar", 
            "Raj", "Siti", "Tan", "Wong", "Yusuf", "Zainal", "Zara", "Danish", "Emma", 
            "Faris", "Gopal", "Hana", "Iman", "Jayden", "Khadijah", "Liyana", "Muthu",
            "Nora", "Ooi", "Puteri", "Qistina", "Rahim", "Syahira", "Tengku", "Uma", "Vijay", "Wei"
        ]
        
        surnames = [
            "bin Ahmad", "binti Ali", "bin Hassan", "binti Mohamed", "bin Ismail",
            "binti Abdullah", "bin Tan", "binti Lee", "bin Wong", "binti Raj",
            "bin Omar", "binti Yusuf", "bin Chong", "binti Lim"
        ]
        
        hobbies = [
            "Reading", "Football", "Badminton", "Swimming", "Drawing", "Gaming",
            "Cycling", "Dancing", "Singing", "Cooking", "Photography", "Chess",
            "Basketball", "Music", "Art", "Science", "Mathematics"
        ]
        
        colours = [
            "Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Pink", 
            "Black", "White", "Brown", "Gray", "Gold", "Silver", "Maroon"
        ]
        
        schools = [
            "SK Taman Jaya", "SK Putrajaya", "SK Seri Indah", "SMK Bukit Bintang",
            "SMK Taman Melawati", "SMK Seksyen 13", "SJK(C) Chung Hwa", 
            "SJK(T) Vivekananda", "International School of KL", "MRSM Ulul Albab",
            "SK Seri Permai", "SMK Sultan Abdul Samad", "SK Taman Megah", "SMK Bandar Utama"
        ]
        
        current_year = datetime.now().year
        
        # Generate 50 random student records
        for _ in range(50):
            name = f"{random.choice(malay_names)} {random.choice(surnames)}"
            age = random.randint(5, 18)
            year_of_birth = current_year - age
            fav_hobby = random.choice(hobbies)
            colour = random.choice(colours)
            school = random.choice(schools)
            donation_count = random.randint(0, 8)
            
            # Determine member grade based on donation count
            if donation_count == 0:
                member_grade = "Green"
            elif 1 <= donation_count <= 3:
                member_grade = "Silver"
            elif 4 <= donation_count <= 6:
                member_grade = "Gold"
            else:
                member_grade = "Diamond"
            
            c.execute('''INSERT INTO students 
                         (name, age, year_of_birth, favourite_hobby, favourite_colour, 
                          school, donation_count, member_grade, registration_date)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (name, age, year_of_birth, fav_hobby, colour, school, 
                      donation_count, member_grade, datetime.now()))
            
            # Generate photos for each donation
            student_id = c.lastrowid
            for _ in range(donation_count):
                # Generate a simple smile image (placeholder)
                smile_photo = generate_smile_image()
                message = random.choice([
                    "Bringing joy with my toys!",
                    "Sharing happiness with orphans",
                    "Making someone smile today",
                    "Giving old toys a new purpose",
                    "Spreading love through donation"
                ])
                smile_rating = random.randint(1, 10)
                
                c.execute('''INSERT INTO photos 
                             (student_id, photo_base64, message, smile_rating, uploaded_date)
                             VALUES (?, ?, ?, ?, ?)''',
                         (student_id, smile_photo, message, smile_rating, datetime.now()))
    
    conn.commit()
    conn.close()

# Function to generate a simple smile image (placeholder)
def generate_smile_image():
    # Create a simple colored image with a smiley face
    img = Image.new('RGB', (200, 200), color=random.choice(['#FFD700', '#87CEEB', '#98FB98', '#FFB6C1']))
    draw = ImageDraw.Draw(img)
    
    # Draw face
    draw.ellipse([50, 50, 150, 150], fill='#FFE4B5', outline='#000000', width=2)
    
    # Draw eyes
    draw.ellipse([80, 80, 90, 90], fill='#000000')
    draw.ellipse([110, 80, 120, 90], fill='#000000')
    
    # Draw smile
    draw.arc([70, 70, 130, 130], start=0, end=180, fill='#000000', width=3)
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str

# Function to display base64 image
def display_base64_image(base64_string):
    img_data = base64.b64decode(base64_string)
    img = Image.open(BytesIO(img_data))
    return img

# Function to get all students
def get_students():
    conn = sqlite3.connect('charity_students.db')
    df = pd.read_sql_query("SELECT * FROM students", conn)
    conn.close()
    return df

# Function to get all photos
def get_photos():
    conn = sqlite3.connect('charity_students.db')
    df = pd.read_sql_query("""
        SELECT p.*, s.name, s.donation_count, s.member_grade 
        FROM photos p 
        JOIN students s ON p.student_id = s.id 
        ORDER BY p.smile_rating DESC
    """, conn)
    conn.close()
    return df

# Function to register new student
def register_student(name, age, hobby, colour, school):
    conn = sqlite3.connect('charity_students.db')
    c = conn.cursor()
    
    year_of_birth = datetime.now().year - age
    donation_count = 0
    member_grade = "Green"
    
    c.execute('''INSERT INTO students 
                 (name, age, year_of_birth, favourite_hobby, favourite_colour, 
                  school, donation_count, member_grade, registration_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
             (name, age, year_of_birth, hobby, colour, school, 
              donation_count, member_grade, datetime.now()))
    
    conn.commit()
    conn.close()

# Function to add photo for existing member
def add_photo(student_id, photo_base64, message, smile_rating):
    conn = sqlite3.connect('charity_students.db')
    c = conn.cursor()
    
    # Add photo
    c.execute('''INSERT INTO photos 
                 (student_id, photo_base64, message, smile_rating, uploaded_date)
                 VALUES (?, ?, ?, ?, ?)''',
             (student_id, photo_base64, message, smile_rating, datetime.now()))
    
    # Update donation count and member grade
    c.execute("SELECT donation_count FROM students WHERE id = ?", (student_id,))
    current_count = c.fetchone()[0]
    new_count = current_count + 1
    
    # Update member grade based on new count
    if new_count == 0:
        new_grade = "Green"
    elif 1 <= new_count <= 3:
        new_grade = "Silver"
    elif 4 <= new_count <= 6:
        new_grade = "Gold"
    else:
        new_grade = "Diamond"
    
    c.execute('''UPDATE students 
                 SET donation_count = ?, member_grade = ? 
                 WHERE id = ?''',
             (new_count, new_grade, student_id))
    
    conn.commit()
    conn.close()

# Initialize database
init_database()

# Main page layout
st.title("❤️ 1000 Smiles : Toy Donation Charity - Bring Smiles to Orphans")
st.markdown("---")

# Left column for messages and information
col_left, col_right = st.columns([2, 1])

with col_left:
    # Encouraging message to students
    st.subheader("💝 A Message to Students:")
    st.markdown("""
    *Dear young friends,*  
    
    Your old toys hold magical powers—they can transform tears into smiles at our orphanages. 
    Each toy you donate becomes a cherished companion for a child who needs comfort and joy. 
    You have the amazing ability to create happiness and make a real difference in someone's life. 
    Join our mission to spread love, one toy at a time!
    
    *You are the heroes who bring smiles to those who need them most.*
    """)
    
    # Encouraging message to parents
    st.subheader("👨‍👩‍👧‍👦 A Message to Parents:")
    st.markdown("""
    *Dear Parents,*  
    
    You're nurturing the next generation of compassionate leaders. Encouraging your child to donate teaches 
    empathy, generosity, and social responsibility. Watch their confidence grow as they experience the joy 
    of giving. Together, we can instill values that last a lifetime while making a tangible difference 
    in our community. Your support in this journey is invaluable.
    
    *Thank you for raising kind-hearted children.*
    """)

with col_right:
    # Member Grade Rules
    st.subheader("🏆 Member Grade Progression")
    st.info("""
    **Green Member:** 0 donations (New Member)  
    **Silver Member:** 1-3 donations  
    **Gold Member:** 4-6 donations  
    **Diamond Member:** 7+ donations  
    
    *Each donation = 1 smile photo captured*
    """)
    
    # Contact Information
    st.subheader("📞 Contact to Donate")
    st.markdown("""
    **Email:** donations@toycharity.my  
    **Address:**  
    Toy Donation Center  
    123 Jalan Kebajikan  
    50480 Kuala Lumpur  
    Malaysia
    
    **Phone:** +60 3-1234 5678  
    **Operating Hours:** 9am - 5pm (Mon-Sat)
    """)

st.markdown("---")

# Registration Links Section
st.subheader("📋 Join Our Mission")

col_reg1, col_reg2 = st.columns(2)

with col_reg1:
    with st.expander("🎓 Register as New Member", expanded=False):
        with st.form("new_member_form"):
            name = st.text_input("Full Name")
            age = st.slider("Age", 5, 18, 10)
            hobby = st.selectbox("Favourite Hobby", [
                "Reading", "Football", "Badminton", "Swimming", "Drawing", "Gaming",
                "Cycling", "Dancing", "Singing", "Cooking", "Photography", "Chess"
            ])
            colour = st.selectbox("Favourite Colour", [
                "Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Pink", 
                "Black", "White", "Brown", "Gray", "Gold", "Silver"
            ])
            school = st.text_input("School Name", "SK Taman Jaya")
            
            submitted = st.form_submit_button("Register Now")
            if submitted:
                if name:
                    register_student(name, age, hobby, colour, school)
                    st.success(f"🎉 Welcome {name}! You are now a Green Member!")
                else:
                    st.error("Please enter your name")

with col_reg2:
    with st.expander("📸 Existing Member - Add Donation & Photo", expanded=False):
        with st.form("add_photo_form"):
            conn = sqlite3.connect('charity_students.db')
            students = pd.read_sql_query("SELECT id, name FROM students", conn)
            conn.close()
            
            student_options = {row['id']: row['name'] for _, row in students.iterrows()}
            student_id = st.selectbox("Select Your Name", options=list(student_options.keys()),
                                     format_func=lambda x: student_options[x])
            
            message = st.text_area("Your Message to the Orphan", 
                                 "I hope this toy brings you as much joy as it brought me!")
            
            smile_rating = st.slider("Rate the Orphan's Smile (1-10)", 1, 10, 8)
            
            # Option to upload or generate photo
            photo_option = st.radio("Photo Option:", ["Generate Random Smile", "Upload Photo"])
            
            if photo_option == "Generate Random Smile":
                photo_base64 = generate_smile_image()
                photo_preview = display_base64_image(photo_base64)
                st.image(photo_preview, caption="Generated Smile", width=150)
            else:
                uploaded_file = st.file_uploader("Upload Smile Photo", type=['jpg', 'png', 'jpeg'])
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    photo_base64 = base64.b64encode(buffered.getvalue()).decode()
                    st.image(img, caption="Uploaded Photo", width=150)
                else:
                    photo_base64 = None
            
            submitted_photo = st.form_submit_button("Submit Donation & Photo")
            if submitted_photo:
                if photo_base64:
                    add_photo(student_id, photo_base64, message, smile_rating)
                    st.success("✅ Donation recorded! Thank you for spreading smiles!")
                else:
                    st.error("Please generate or upload a photo")

st.markdown("---")

# Get data
students_df = get_students()
photos_df = get_photos()

# Display top 10 donors
st.subheader("🏅 Top 10 Student Donors")
top_donors = students_df.nlargest(10, 'donation_count')[['name', 'age', 'donation_count', 'member_grade', 'school']]
top_donors.index = range(1, len(top_donors) + 1)

st.dataframe(top_donors.style.apply(
    lambda x: ['background: #FFD700' if x['member_grade'] == 'Diamond' 
               else 'background: #C0C0C0' if x['member_grade'] == 'Gold'
               else 'background: #E5E4E2' if x['member_grade'] == 'Silver'
               else 'background: #90EE90' for _ in x],
    axis=1
), use_container_width=True)

# Create columns for charts
col1, col2 = st.columns(2)

with col1:
    # Donation Distribution
    st.subheader("📊 Donation Count Distribution")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    donation_counts = students_df['donation_count'].value_counts().sort_index()
    bars = ax1.bar(donation_counts.index.astype(str), donation_counts.values)
    
    # Color bars based on member grade
    colors = []
    for count in donation_counts.index:
        if count == 0:
            colors.append('green')
        elif 1 <= count <= 3:
            colors.append('silver')
        elif 4 <= count <= 6:
            colors.append('gold')
        else:
            colors.append('violet')
    
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    ax1.set_xlabel('Donation Count')
    ax1.set_ylabel('Number of Students')
    ax1.set_title('Distribution of Toy Donations')
    plt.xticks(rotation=0)
    st.pyplot(fig1)

with col2:
    # Member Grade Distribution
    st.subheader("🎖️ Member Grade Distribution")
    grade_counts = students_df['member_grade'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    
    colors_grade = []
    for grade in grade_counts.index:
        if grade == 'Diamond':
            colors_grade.append('violet')
        elif grade == 'Gold':
            colors_grade.append('gold')
        elif grade == 'Silver':
            colors_grade.append('silver')
        else:
            colors_grade.append('green')
    
    ax2.bar(grade_counts.index, grade_counts.values, color=colors_grade, alpha=0.8)
    ax2.set_xlabel('Member Grade')
    ax2.set_ylabel('Number of Students')
    ax2.set_title('Distribution of Member Grades')
    st.pyplot(fig2)

# Age vs Donation Correlation
st.subheader("📈 Age vs Donation Correlation")
fig3, ax3 = plt.subplots(figsize=(12, 4))

# Scatter plot with color by member grade
colors_dict = {'Green': 'green', 'Silver': 'silver', 'Gold': 'gold', 'Diamond': 'violet'}
student_colors = [colors_dict[grade] for grade in students_df['member_grade']]

scatter = ax3.scatter(students_df['age'], students_df['donation_count'], 
                     c=student_colors, s=100, alpha=0.6, edgecolors='black')
ax3.set_xlabel('Age')
ax3.set_ylabel('Donation Count')
ax3.set_title('Correlation between Age and Toy Donations')
ax3.grid(True, alpha=0.3)

# Add legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='green', label='Green Member'),
                   Patch(facecolor='silver', label='Silver Member'),
                   Patch(facecolor='gold', label='Gold Member'),
                   Patch(facecolor='violet', label='Diamond Member')]
ax3.legend(handles=legend_elements, loc='upper right')

st.pyplot(fig3)

# Calculate and display correlation
correlation = students_df['age'].corr(students_df['donation_count'])
st.metric("Correlation Coefficient (Age vs Donations)", f"{correlation:.3f}")

# Top 5 Smile Photos
st.subheader("😊 Top 5 Best Smile Photos")
top_photos = photos_df.nlargest(5, 'smile_rating')

if not top_photos.empty:
    cols = st.columns(5)
    for idx, (_, row) in enumerate(top_photos.iterrows()):
        with cols[idx]:
            img = display_base64_image(row['photo_base64'])
            st.image(img, width=150)
            st.caption(f"**{row['name']}**")
            st.caption(f"Rating: {row['smile_rating']}/10 ⭐")
            st.caption(f"'{row['message']}'")
            st.caption(f"Donations: {row['donation_count']} | {row['member_grade']} Member")
else:
    st.info("No photos uploaded yet. Be the first to donate and capture a smile!")

# Display raw data
st.markdown("---")
st.subheader("📋 All Student Data")
if st.checkbox("Show complete student database"):
    display_df = students_df.drop(columns=['id', 'registration_date'])
    st.dataframe(display_df, use_container_width=True)

# Sidebar information
with st.sidebar:
    st.header("📊 Dashboard Summary")
    
    total_students = len(students_df)
    total_donations = students_df['donation_count'].sum()
    avg_donations = students_df['donation_count'].mean()
    
    st.metric("Total Students", total_students)
    st.metric("Total Donations", total_donations)
    st.metric("Average Donations/Student", f"{avg_donations:.1f}")
    
    st.subheader("🎯 Quick Stats")
    st.write(f"**Most Common Hobby:** {students_df['favourite_hobby'].mode().values[0]}")
    st.write(f"**Most Popular Color:** {students_df['favourite_colour'].mode().values[0]}")
    st.write(f"**Youngest Student:** {students_df['age'].min()} years")
    st.write(f"**Oldest Student:** {students_df['age'].max()} years")
    
    # Progress bars for member grades
    st.subheader("🏅 Member Grade Progress")
    for grade in ['Diamond', 'Gold', 'Silver', 'Green']:
        count = len(students_df[students_df['member_grade'] == grade])
        percentage = (count / total_students) * 100
        st.progress(percentage/100, text=f"{grade}: {count} students ({percentage:.1f}%)")
    
    if st.button("🔄 Refresh Dashboard"):
        st.rerun()

# Footer
st.markdown("---")
st.caption("❤️ Toy Donation Charity Malaysia | Bringing Smiles to Orphanages Since 2024")
st.caption("Every toy donated = One smile captured = A lifetime of happiness shared")

