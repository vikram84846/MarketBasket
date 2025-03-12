import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.title("Retail Product Pair Advisor")
    st.markdown("Smart suggestions for product combinations")
    
    # Load your rules data
    rules = pd.read_csv('associationRules.csv')  # Replace with your actual data source
    
    # Convert metrics to business-friendly terms
    rules['success_rate'] = (rules['confidence'] * 100).round(1)
    rules['combination_frequency'] = (rules['support'] * 100).round(3)
    
    # Sidebar controls
    with st.sidebar:
        st.header("Adjust Recommendations")
        min_success = st.slider("Minimum Probability (%)", 1, 100, 40, 
                               help="Chance customers will buy both items together")
        min_frequency = st.slider("Minimum Frequency (%)", 0.0, 5.0, 0.5, step=0.1,
                                format="%.2f%%", 
                                help="How often this combination appears in all transactions")
    
    # Filter rules
    filtered = rules[
        (rules['success_rate'] >= min_success) &
        (rules['combination_frequency'] >= min_frequency)
    ].sort_values('success_rate', ascending=False)
    
    # Main display
    st.header(f"Showing {len(filtered)} Product Pairings")
    
    # Add custom CSS for grid layout
    st.markdown("""
    <style>
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
            padding: 1rem;
        }
        
        .card {
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 1.2rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            cursor: pointer;
        }
        
        .antecedent {
            color: #2c3e50;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .consequent {
            color: #27ae60;
            font-weight: 600;
            margin: 0.8rem 0;
        }
        
        .metrics {
            display: flex;
            justify-content: space-between;
            margin-top: 1rem;
            font-size: 0.9rem;
        }
        
        .success-rate {
            color: #2980b9;
        }
        
        .frequency {
            color: #7f8c8d;
        }
    </style>
    """, unsafe_allow_html=True)
    
    if not filtered.empty:
        # Create grid container
        st.markdown('<div class="grid-container">', unsafe_allow_html=True)
        
        for _, row in filtered.iterrows():
            card_html = f"""
            <div class="card">
                <div class="antecedent">🛒 Customers buying: {row['antecedents']}</div>
                <div class="consequent">➕ Likely to add: {row['consequents']}</div>
                <div class="metrics">
                    <div class="success-rate">🎯 {row['success_rate']}% Success</div>
                    <div class="frequency">📊 {row['combination_frequency']}% Frequency</div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
        
        # Close grid container
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No recommendations meet current criteria. Try lowering the filters in the sidebar.")

    # Visualization
    if not filtered.empty:
        st.header("Relationship Explorer")
        fig = px.scatter(filtered,
                         x='combination_frequency',
                         y='success_rate',
                         size='lift',
                         color='lift',
                         hover_name='antecedents',
                         hover_data={
                             'consequents': True,
                             'success_rate': True,
                             'combination_frequency': True,
                             'lift': True
                         },
                         labels={
                             'combination_frequency': 'Frequency (%)',
                             'success_rate': 'Success Rate (%)',
                             'lift': 'Strength'
                         })
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()