from flask import Flask, render_template, request, url_for
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
import os

app = Flask(__name__, static_folder='static')

# Data file path
DATA_FILE = 'event_data.csv'

def load_data():
    """Load data from CSV file or create if not exists"""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Create sample data structure
        data = pd.DataFrame(columns=['Name', 'EventName', 'RSVPStatus', 'Attended'])
        # Add some sample data
        sample_data = [
            ["John Doe", "Tech Conference", "Yes", "Yes"],
            ["Jane Smith", "Tech Conference", "Yes", "No"],
            ["Bob Johnson", "Tech Conference", "No", "No"],
            ["Alice Brown", "Tech Conference", "Maybe", "No"],
            ["Charlie Wilson", "Tech Conference", "Yes", "Yes"],
        ]
        sample_df = pd.DataFrame(sample_data, columns=data.columns)
        sample_df.to_csv(DATA_FILE, index=False)
        return sample_df

def save_data(df):
    """Save data to CSV file"""
    df.to_csv(DATA_FILE, index=False)

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    """Main dashboard route handling data display and form submission"""
    df = load_data()
    
    # Handle form submission
    if request.method == 'POST':
        if 'delete' in request.form:
            # Handle deletion
            name_to_delete = request.form['delete']
            df = df[df['Name'] != name_to_delete]
        else:
            # Handle new entry
            new_entry = {
                "Name": request.form.get('name'),
                "EventName": request.form.get('event'),
                "RSVPStatus": request.form.get('rsvp'),
                "Attended": request.form.get('attended')
            }
            # Validate data
            if all(new_entry.values()):  # Check all fields are filled
                new_df = pd.DataFrame([new_entry])
                df = pd.concat([df, new_df], ignore_index=True)
        
        save_data(df)
    
    # Calculate KPIs
    total_invited = len(df)
    total_attended = len(df[df['Attended'] == 'Yes'])
    no_shows = len(df[(df['RSVPStatus'] == 'Yes') & (df['Attended'] == 'No')])
    attendance_rate = (total_attended / total_invited * 100) if total_invited > 0 else 0
    
    # Generate visualizations
    rsvp_img = generate_pie_chart(df, 'RSVPStatus', 'RSVP Status Breakdown')
    attended_img = generate_pie_chart(df, 'Attended', 'Attendance Breakdown')
    
    return render_template('index.html', 
                         table_data=df.to_dict('records'),
                         total_invited=total_invited,
                         total_attended=total_attended,
                         no_shows=no_shows,
                         attendance_rate=f"{attendance_rate:.1f}%",
                         rsvp_img=rsvp_img,
                         attended_img=attended_img)

def generate_pie_chart(df, column, title):
    """Generate a pie chart and return as base64 encoded image"""
    plt.figure(figsize=(6, 6))
    
    # Count values and handle missing data
    counts = df[column].value_counts().sort_index()
    
    # Custom colors based on status
    if column == 'RSVPStatus':
        colors = {'Yes': '#4CAF50', 'No': '#F44336', 'Maybe': '#FFC107'}
        color_list = [colors.get(x, '#2196F3') for x in counts.index]
    else:
        colors = {'Yes': '#4CAF50', 'No': '#F44336'}
        color_list = [colors.get(x, '#2196F3') for x in counts.index]
    
    # Create pie chart with improved styling
    patches, texts, autotexts = plt.pie(
        counts, 
        labels=counts.index, 
        autopct='%1.1f%%', 
        startangle=90,
        colors=color_list,
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
        textprops={'fontsize': 10}
    )
    
    # Improve autotext color for better visibility
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
    
    plt.title(title, pad=20)
    plt.axis('equal')
    
    # Save to buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    plt.close()
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True)