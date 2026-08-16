import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ──
st.set_page_config(
    page_title="Traceit.live Demo",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1a1a2e; }
    .sub-header { font-size: 1.1rem; color: #4a4a6a; margin-bottom: 2rem; }
    .metric-card { background: #f8f9fa; border-radius: 12px; padding: 1.5rem; border-left: 4px solid #00b894; }
    .leak-card { background: #fff5f5; border-radius: 12px; padding: 1.5rem; border-left: 4px solid #e74c3c; }
    .savings-card { background: #f0fff4; border-radius: 12px; padding: 1.5rem; border-left: 4px solid #00b894; }
    .ledger-row { font-family: monospace; font-size: 0.85rem; }
    .compliance-pass { color: #00b894; font-weight: 600; }
    .compliance-fail { color: #e74c3c; font-weight: 600; }
    div[data-testid="stTabs"] button { font-size: 1rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.image("https://via.placeholder.com/180x60/1a1a2e/ffffff?text=Traceit.live", width=180)
    st.markdown("### 🏭 Plant Configuration")

    plant_name = st.text_input("Plant Name", value="Colombo Plant 01")
    num_machines = st.number_input("Machines", min_value=5, max_value=500, value=45)
    num_items = st.number_input("Trackable Items (SKUs)", min_value=10, max_value=5000, value=320)
    annual_spend = st.number_input("Annual Indirect Spend ($)", min_value=10000, max_value=10000000, value=850000, step=10000)
    employees = st.number_input("Floor Employees", min_value=10, max_value=5000, value=280)

    st.markdown("---")
    st.markdown("**💡 About this demo**")
    st.markdown("""
    This app demonstrates the four pillars of the 
    Traceit pre-sales strategy:

    1. **Leak Calculator** — quantify hidden losses
    2. **Plant Dashboard** — real-time inventory visibility
    3. **Immutable Ledger** — fraud-resistant audit trail
    4. **Needle Compliance** — brand audit readiness
    """)

# ── Header ──
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<p class="main-header">📦 Traceit.live — Pre-Sales Demo</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">From "spreadsheet and gut feel" to immutable plant accountability in one platform.</p>', unsafe_allow_html=True)
with col2:
    st.metric("Plants Live", "22", "+3 this month")
    st.metric("Countries", "3", "LK • IN • BD")

st.markdown("---")

# ── Tabs ──
tab1, tab2, tab3, tab4 = st.tabs(["💰 Leak Calculator", "📊 Plant Dashboard", "📜 Immutable Ledger", "🪡 Needle Compliance"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: LEAK CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("## The 'Leak Calculator' — Your Pre-Sales Hook")
    st.markdown("*Before any demo, send this to the prospect. If the math shocks them, they are primed.*")

    c1, c2, c3 = st.columns(3)

    # Calculations based on industry averages for apparel manufacturing
    leakage_rate = 0.08  # 8% average leakage on indirect spend
    search_time_mins = 12  # avg time to find an item record in spreadsheet
    searches_per_day = 45
    hourly_rate = 4.50  # USD, floor supervisor rate in LK/BD/IN

    annual_leak = annual_spend * leakage_rate
    daily_search_hours = (searches_per_day * search_time_mins) / 60
    annual_search_cost = daily_search_hours * hourly_rate * 260  # working days
    duplicate_buy_rate = 0.05
    annual_duplicate_cost = annual_spend * duplicate_buy_rate

    total_annual_leak = annual_leak + annual_search_cost + annual_duplicate_cost
    traceit_cost = num_items * 1.0  # $1 per item per year
    roi_ratio = total_annual_leak / traceit_cost if traceit_cost > 0 else 0

    with c1:
        st.markdown('<div class="leak-card">', unsafe_allow_html=True)
        st.markdown(f"**💸 Annual Leak (Unwatched)**")
        st.markdown(f"<h2 style='color:#e74c3c; margin:0;'>${total_annual_leak:,.0f}</h2>", unsafe_allow_html=True)
        st.markdown(f"""
        • Material leakage: **${annual_leak:,.0f}** (8% of indirect spend)
        • Search time cost: **${annual_search_cost:,.0f}** (12 min/search, 45 searches/day)
        • Duplicate purchases: **${annual_duplicate_cost:,.0f}** (5% of spend)
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f"**📦 Traceit Subscription**")
        st.markdown(f"<h2 style='color:#1a1a2e; margin:0;'>${traceit_cost:,.0f}</h2>", unsafe_allow_html=True)
        st.markdown(f"""
        • **{num_items}** items tracked
        • **Unlimited users** (no licenses)
        • **$1/item/year** — transparent pricing
        • No implementation fees
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="savings-card">', unsafe_allow_html=True)
        st.markdown(f"**✅ ROI Ratio**")
        st.markdown(f"<h2 style='color:#00b894; margin:0;'>{roi_ratio:.1f}×</h2>", unsafe_allow_html=True)
        st.markdown(f"""
        • Every **$1** spent on Traceit
        • Saves **${roi_ratio:.0f}** in leakage
        • Payback period: **< 2 weeks**
        • Net annual savings: **${total_annual_leak - traceit_cost:,.0f}**
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Interactive chart
    st.markdown("### 📈 Leak Breakdown vs. Traceit Cost")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Annual Leak',
        x=['Material Leakage', 'Search Time Cost', 'Duplicate Purchases', 'Traceit Cost'],
        y=[annual_leak, annual_search_cost, annual_duplicate_cost, traceit_cost],
        marker_color=['#e74c3c', '#e67e22', '#f39c12', '#00b894'],
        text=[f'${v:,.0f}' for v in [annual_leak, annual_search_cost, annual_duplicate_cost, traceit_cost]],
        textposition='auto',
    ))
    fig.update_layout(
        height=400,
        template='plotly_white',
        yaxis_title='Annual Cost ($)',
        showlegend=False,
        margin=dict(t=30, b=30)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info("💡 **Sales Tip:** Send this calculator as an interactive PDF before the first call. If the prospect's eyes widen at the ROI number, book the Shadow Day demo immediately.")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: PLANT DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("## Plant Dashboard — Real-Time Inventory Visibility")
    st.markdown("*What your ERP cannot show you: where things actually are, right now.*")

    # Generate demo data
    random.seed(42)
    machines = [f"Machine-JK-{100+i}" for i in range(min(num_machines, 20))]
    lines = [f"Line-{random.choice(['A','B','C','D','E'])}-{random.randint(1,5)}" for _ in machines]

    items_data = []
    item_types = ['Needle Packs', 'Bobbin Cases', 'Presser Feet', 'Machine Oil', 'Thread Cones', 'Spare Motors', 'Belts']

    for i in range(min(num_items, 50)):
        item_type = random.choice(item_types)
        location = random.choice(machines + ['Store Room A', 'Store Room B', 'Receiving'])
        qty = random.randint(1, 500)
        status = random.choice(['Active', 'Low Stock', 'Excess'])

        items_data.append({
            'Item ID': f'ITM-{10000+i}',
            'Type': item_type,
            'Location': location,
            'Quantity': qty,
            'Status': status,
            'Last Moved': (datetime.now() - timedelta(hours=random.randint(1, 720))).strftime('%Y-%m-%d %H:%M')
        })

    df_items = pd.DataFrame(items_data)

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Items Tracked", len(df_items), "+12 today")
    k2.metric("Store Room A Stock", df_items[df_items['Location']=='Store Room A']['Quantity'].sum(), "-8% vs last week")
    k3.metric("Low Stock Alerts", len(df_items[df_items['Status']=='Low Stock']), "🔴 Action needed")
    k4.metric("Excess Stock Found", len(df_items[df_items['Status']=='Excess']), "💰 $12,400 recoverable")

    st.markdown("---")

    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("### 📍 Inventory by Location")
        location_summary = df_items.groupby('Location')['Quantity'].sum().reset_index().sort_values('Quantity', ascending=False).head(10)
        fig2 = px.bar(location_summary, x='Location', y='Quantity', color='Quantity',
                      color_continuous_scale='Teal', template='plotly_white')
        fig2.update_layout(height=350, margin=dict(t=10, b=10), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        st.markdown("### ⚠️ Status Breakdown")
        status_counts = df_items['Status'].value_counts()
        colors = {'Active': '#00b894', 'Low Stock': '#e74c3c', 'Excess': '#f39c12'}
        fig3 = px.pie(values=status_counts.values, names=status_counts.index, 
                      color=status_counts.index, color_discrete_map=colors,
                      template='plotly_white', hole=0.4)
        fig3.update_layout(height=350, margin=dict(t=10, b=10), showlegend=True)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### 📋 Live Inventory Table")
    st.dataframe(df_items, use_container_width=True, hide_index=True)

    st.success("🎯 **This is what your ERP cannot show.** Your ERP knows you bought 1,000 needles. Traceit knows 40 are on Line-A-3, 20 are on Machine-JK-105, and 940 are still in Store Room A. That's the difference between a PO and reality.")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: IMMUTABLE LEDGER
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("## Immutable Ledger — The Accountability Layer")
    st.markdown("*Every transaction recorded with person, reason, timestamp, cost. Impossible to edit after the fact.*")

    # Generate ledger data
    random.seed(123)
    ledger_data = []
    actions = ['Issued', 'Returned', 'Transferred', 'Consumed', 'Received']
    reasons = ['Production Line Request', 'Preventive Maintenance', 'Breakdown Repair', 'Stock Reconciliation', 'New PO Receipt']
    operators = ['R. Perera', 'S. Fernando', 'A. Silva', 'K. Jayawardena', 'M. Bandara']

    for i in range(25):
        ts = datetime.now() - timedelta(minutes=random.randint(5, 10080))
        ledger_data.append({
            'Timestamp': ts.strftime('%Y-%m-%d %H:%M:%S'),
            'Transaction ID': f'TXN-{900000+i}',
            'Item': random.choice(['Needle Packs', 'Bobbin Cases', 'Machine Oil', 'Thread Cones']),
            'Item ID': f'ITM-{10000+random.randint(0, 49)}',
            'Action': random.choice(actions),
            'Quantity': random.randint(1, 50),
            'From': random.choice(['Store Room A', 'Store Room B', 'Line-A-2', 'Line-B-1']),
            'To': random.choice(['Line-A-3', 'Line-C-1', 'Machine-JK-105', 'Machine-JK-112']),
            'Operator': random.choice(operators),
            'Reason': random.choice(reasons),
            'Cost ($)': round(random.uniform(5, 500), 2),
            'Hash': f'0x{random.getrandbits(64):016x}'
        })

    df_ledger = pd.DataFrame(ledger_data).sort_values('Timestamp', ascending=False)

    st.markdown("### 🔒 Recent Transactions (Immutable)")

    # Show as styled table
    for _, row in df_ledger.head(8).iterrows():
        with st.container():
            cols = st.columns([1.5, 1.2, 1.5, 1, 1.2, 1.5, 1.5, 2, 1.5])
            cols[0].markdown(f"<span class='ledger-row'>🕐 {row['Timestamp']}</span>", unsafe_allow_html=True)
            cols[1].markdown(f"<span class='ledger-row'>#{row['Transaction ID']}</span>", unsafe_allow_html=True)
            cols[2].markdown(f"**{row['Item']}**")
            cols[3].markdown(f"{row['Action']}")
            cols[4].markdown(f"Qty: {row['Quantity']}")
            cols[5].markdown(f"→ {row['To']}")
            cols[6].markdown(f"👤 {row['Operator']}")
            cols[7].markdown(f"<span style='font-size:0.75rem; color:#666;'>{row['Reason']}</span>", unsafe_allow_html=True)
            cols[8].markdown(f"<span class='ledger-row'>🔐 {row['Hash'][:12]}...</span>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 4px 0; border: none; border-top: 1px solid #eee;'>", unsafe_allow_html=True)

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📊 Transaction Volume (Last 7 Days)")
        daily_txns = pd.DataFrame({
            'Day': [(datetime.now() - timedelta(days=i)).strftime('%a') for i in range(6, -1, -1)],
            'Transactions': [random.randint(80, 250) for _ in range(7)]
        })
        fig4 = px.line(daily_txns, x='Day', y='Transactions', markers=True, template='plotly_white')
        fig4.update_traces(line_color='#00b894', marker_size=8)
        fig4.update_layout(height=300, margin=dict(t=10, b=10))
        st.plotly_chart(fig4, use_container_width=True)

    with c2:
        st.markdown("### 💰 Cost Tracked by Action")
        action_costs = df_ledger.groupby('Action')['Cost ($)'].sum().reset_index()
        fig5 = px.bar(action_costs, x='Action', y='Cost ($)', color='Action', template='plotly_white')
        fig5.update_layout(height=300, margin=dict(t=10, b=10), showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)

    st.warning("⚠️ **Audit-Ready:** Every entry is hashed and immutable. If a brand auditor asks 'Where was Needle Pack ITM-10042 on August 10th at 2:30 PM?' — you have the answer in 3 seconds. Try doing that with a spreadsheet.")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4: NEEDLE COMPLIANCE
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("## 🪡 Needle Compliance — Brand Audit Readiness")
    st.markdown("*For $1 per needle per year, you have an immutable audit trail that satisfies any brand audit. H&M, Zara, M&S — they all ask the same question: 'Can you prove every needle was accounted for?'*")

    # Generate needle data
    random.seed(77)
    needle_batches = []
    brands = ['H&M', 'Zara', 'M&S', 'Uniqlo', 'Levi's']

    for i in range(30):
        batch = f'NDL-BATCH-{2026}{random.randint(100, 999)}'
        total = random.randint(100, 1000)
        issued = random.randint(20, total-50)
        returned = random.randint(10, issued-5)
        broken = random.randint(1, returned)
        lost = total - issued - (returned - broken) - random.randint(0, 20)

        # Compliance check
        compliant = (lost / total) < 0.02 and broken > 0  # <2% lost, all broken accounted for

        needle_batches.append({
            'Batch ID': batch,
            'Brand': random.choice(brands),
            'Total Needles': total,
            'Issued': issued,
            'Returned': returned,
            'Broken (Accounted)': broken,
            'Lost / Unaccounted': max(0, lost),
            'Compliance Rate': round((total - max(0, lost)) / total * 100, 1),
            'Status': '✅ PASS' if compliant else '❌ FAIL',
            'Last Audit': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
        })

    df_needles = pd.DataFrame(needle_batches)

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    pass_rate = len(df_needles[df_needles['Status']=='✅ PASS']) / len(df_needles) * 100
    k1.metric("Batches Tracked", len(df_needles), "+5 this week")
    k2.metric("Compliance Rate", f"{pass_rate:.0f}%", "▲ 12% vs last quarter")
    k3.metric("Needles at Risk", df_needles['Lost / Unaccounted'].sum(), "🔴 Immediate action")
    k4.metric("Audit Ready", "100%", "All batches logged")

    st.markdown("---")

    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("### 📋 Needle Batch Compliance Status")
        st.dataframe(df_needles[['Batch ID', 'Brand', 'Total Needles', 'Lost / Unaccounted', 'Compliance Rate', 'Status', 'Last Audit']], 
                     use_container_width=True, hide_index=True)

    with c2:
        st.markdown("### 📊 Compliance by Brand")
        brand_comp = df_needles.groupby('Brand').agg({
            'Total Needles': 'sum',
            'Lost / Unaccounted': 'sum'
        }).reset_index()
        brand_comp['Compliance %'] = round((1 - brand_comp['Lost / Unaccounted'] / brand_comp['Total Needles']) * 100, 1)

        fig6 = px.bar(brand_comp, x='Brand', y='Compliance %', color='Compliance %',
                      color_continuous_scale=['#e74c3c', '#f39c12', '#00b894'], range_y=[80, 100],
                      template='plotly_white')
        fig6.update_layout(height=350, margin=dict(t=10, b=10), showlegend=False)
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown("---")

    # Audit simulation
    st.markdown("### 📝 Simulated Brand Audit Report")
    st.markdown("*Auto-generated for any brand audit. One click. Zero spreadsheets.*")

    selected_brand = st.selectbox("Select Brand for Audit Report", brands)
    brand_data = df_needles[df_needles['Brand']==selected_brand]

    audit_col1, audit_col2, audit_col3 = st.columns(3)
    audit_col1.metric("Total Batches", len(brand_data))
    audit_col2.metric("Total Needles", brand_data['Total Needles'].sum())
    audit_col3.metric("Unaccounted", brand_data['Lost / Unaccounted'].sum(), delta_color="inverse")

    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #00b894;">
    <h4 style="margin-top:0;">📄 Audit Summary for {selected_brand}</h4>
    <p><strong>Audit Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    <p><strong>Auditor:</strong> Traceit Immutable Ledger (Auto-Generated)</p>
    <p><strong>Total Needles Tracked:</strong> {brand_data['Total Needles'].sum():,}</p>
    <p><strong>Needles Issued:</strong> {brand_data['Issued'].sum():,}</p>
    <p><strong>Needles Returned:</strong> {brand_data['Returned'].sum():,}</p>
    <p><strong>Broken (Accounted):</strong> {brand_data['Broken (Accounted)'].sum():,}</p>
    <p><strong>Lost / Unaccounted:</strong> <span style="color: {'#e74c3c' if brand_data['Lost / Unaccounted'].sum() > 0 else '#00b894'};">{brand_data['Lost / Unaccounted'].sum():,}</span></p>
    <p><strong>Compliance Status:</strong> <span style="color: {'#00b894' if brand_data['Lost / Unaccounted'].sum() == 0 else '#e74c3c'}; font-weight: 600;">{'✅ FULL COMPLIANCE' if brand_data['Lost / Unaccounted'].sum() == 0 else '⚠️ REVIEW REQUIRED'}</span></p>
    <p style="font-size: 0.8rem; color: #666; margin-top: 1rem;">This report is generated from the immutable Traceit ledger. All entries are cryptographically hashed and cannot be altered after recording. Ledger hash: <code>0x{random.getrandbits(128):032x}</code></p>
    </div>
    """, unsafe_allow_html=True)

    st.info("💡 **Sales Tip:** Position Traceit as 'Compliance Insurance.' For $1 per needle per year, a brand audit that would take 3 days of manual spreadsheet digging now takes 3 seconds. One failed brand audit can cost a manufacturer their entire contract. Traceit is the cheapest insurance policy in apparel manufacturing.")

# ── Footer ──
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888; font-size: 0.85rem;'>Traceit.live Demo — Built for o2 Store (PVT) Ltd. | Proposal by Wathsalya Deshappriya</p>", unsafe_allow_html=True)
