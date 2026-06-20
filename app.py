import streamlit as st
import plotly.express as px
import pandas as pd
from src.inventory import load_data, add_product
from src.analytics import register_sale

# 1. Настройка конфигурации страницы
st.set_page_config(
    page_title="Stock+ Management System", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. Словарь переводов (Мультиязычность)
LANGUAGES = {
    "EN": {
        "slogan": "«All product information in one place»",
        "nav_title": "Navigation Menu",
        "user_role": "👤 **User:** Alina B.<br>⚙️ **Role:** Administrator",
        "caption_dash": "Here's what's happening with your warehouse today.",
        "card_capacity": "WAREHOUSE CAPACITY",
        "card_capacity_foot": "Total volume of stocks",
        "card_orders": "TODAY'S ORDERS",
        "card_orders_foot": "Active shipment sessions",
        "card_alert": "LOW STOCK ALERT",
        "card_alert_foot": "Require purchase (< 5 pcs)",
        "card_revenue": "TOTAL REVENUE",
        "card_revenue_foot": "Financial balance",
        "chart_title": "Activity Trend (Stock Levels)",
        "chart_x": "Product",
        "chart_y": "Quantity",
        "chart_info": "Add products in the 'Products' tab to visualize trends.",
        "log_title": "📋 Real-time Activity Log",
        "log_critical": "🔴 **{}** — critical stock: {} pcs. Restock required!",
        "log_ok": "🟢 All warehouse metrics are normal. No critical shortages.",
        "prod_title": "📦 Products & Inventory",
        "prod_caption": "Product database, adding new items, and tracking purchase prices.",
        "prod_expander": "➕ Add New Product Position",
        "lbl_art": "Article (Unique Code)",
        "lbl_name": "Product Name",
        "lbl_stock": "Stock Quantity (pcs)",
        "lbl_p_price": "Purchase Price",
        "lbl_s_price": "Selling Price",
        "btn_save": "💾 Save to Stock+ System",
        "msg_success_add": "Product «{}» successfully added to the system!",
        "msg_error_add": "Error: 'Article' and 'Product Name' fields are required.",
        "tbl_title": "📋 Current Stock Balance",
        "tbl_empty": "Warehouse is empty. Use the form above to add items.",
        "col_art": "Article",
        "col_name": "Product Name",
        "col_stock": "Stock (pcs)",
        "col_p_price": "Purchase Price",
        "col_s_price": "Selling Price",
        "ord_title": "🛒 Orders & Sales Management",
        "ord_caption": "Registration of sales, automatic deduction from stock, and profit tracking.",
        "ord_select": "Select product for shipment/sale",
        "ord_available": "Available in warehouse: **{}** pcs.",
        "ord_qty": "Quantity to ship (pcs)",
        "ord_btn": "📦 Process Order & Deduct Stock",
        "ord_success": "Order processed! Deducted {} pcs of '{}'.",
        "ord_error": "Cannot process order: insufficient quantity in warehouse.",
        "ord_empty": "No products available for sale. Add them in 'Products' tab first.",
        "an_title": "📊 Advanced Analytics",
        "an_caption": "Analysis of profitability, net profit, and business efficiency.",
        "an_pie": "Total Revenue by Product",
        "an_bar": "Net Profit from Transactions",
        "an_log": "📜 Transaction Log",
        "an_empty": "Analytics data is empty. Process some orders in 'Orders' tab.",
        "rep_title": "🗂️ Reports & Export",
        "rep_caption": "Generation of ready stock reports for accounting and management.",
        "rep_success": "CSV/JSON Stock report generated automatically.",
        "rep_btn": "📥 Download Excel/CSV Report",
        "rep_empty": "No data available to generate reports."
    },
    "RU": {
        "slogan": "«Вся информация о товарах в одном месте»",
        "nav_title": "Меню навигации",
        "user_role": "👤 **Пользователь:** Alina B.<br>⚙️ **Роль:** Администратор",
        "caption_dash": "Вот что происходит на вашем складе сегодня.",
        "card_capacity": "ОБЪЕМ СКЛАДА",
        "card_capacity_foot": "Общий объем запасов",
        "card_orders": "ЗАКАЗЫ СЕГОДНЯ",
        "card_orders_foot": "Активные сессии отгрузок",
        "card_alert": "КРИТИЧЕСКИЙ ОСТАТОК",
        "card_alert_foot": "Требуют закупки (< 5 шт)",
        "card_revenue": "ОБЩАЯ ВЫРУЧКА",
        "card_revenue_foot": "Финансовый баланс",
        "chart_title": "Тренды активности (Остатки на складе)",
        "chart_x": "Товар",
        "chart_y": "Количество",
        "chart_info": "Добавьте товары во вкладке Products для визуализации трендов.",
        "log_title": "📋 Лог активности в реальном времени",
        "log_critical": "🔴 **{}** — критический остаток: {} шт. Требуется ресток!",
        "log_ok": "🟢 Все показатели склада в норме. Критических дефицитов нет.",
        "prod_title": "📦 Товары и Инвентарь",
        "prod_caption": "База данных товаров, добавление новых позиций и учет закупочных цен.",
        "prod_expander": "➕ Добавить новую позицию товара",
        "lbl_art": "Артикул (Уникальный код)",
        "lbl_name": "Наименование товара",
        "lbl_stock": "Остаток на складе (шт)",
        "lbl_p_price": "Закупочная стоимость",
        "lbl_s_price": "Актуальная стоимость продажи",
        "btn_save": "💾 Сохранить в систему Stock+",
        "msg_success_add": "Товар «{}» успешно добавлен в систему!",
        "msg_error_add": "Ошибка: Поля 'Артикул' и 'Наименование товара' обязательны.",
        "tbl_title": "📋 Текущий остаток товара на складе",
        "tbl_empty": "Склад пуст. Используйте форму выше для занесения позиций.",
        "col_art": "Артикул",
        "col_name": "Наименование товара",
        "col_stock": "Остаток (шт)",
        "col_p_price": "Цена закупки",
        "col_s_price": "Цена продажи",
        "ord_title": "🛒 Управление заказами и продажами",
        "ord_caption": "Регистрация факта продажи, автоматическое списание со склада и фиксация прибыли.",
        "ord_select": "Выберите товар для отгрузки/продажи",
        "ord_available": "Доступно для списания на складе: **{}** шт.",
        "ord_qty": "Количество к отгрузке (шт)",
        "ord_btn": "📦 Оформить заказ и списать остаток",
        "ord_success": "Заказ оформлен! Списано {} шт. товара '{}'.",
        "ord_error": "Невозможно оформить заказ: недостаточно товара на складе.",
        "ord_empty": "На складе нет доступных товаров для совершения продаж.",
        "an_title": "📊 Продвинутая Аналитика",
        "an_caption": "Анализ маржинальности, чистой прибыли и эффективности бизнеса.",
        "an_pie": "Общая выручка по товарам",
        "an_bar": "Чистая прибыль со сделок",
        "an_log": "📜 Лог совершенных транзакций",
        "an_empty": "Данные аналитики пустые. Оформите заказы во вкладке 'Orders'.",
        "rep_title": "🗂️ Отчеты и Экспорт",
        "rep_caption": "Генерация готовых отчетов по остаткам для бухгалтерии и руководства.",
        "rep_success": "CSV/JSON Отчет по складским остаткам сформирован автоматически.",
        "rep_btn": "📥 Скачать Excel/CSV отчет по складу",
        "rep_empty": "Нет данных для формирования отчетов."
    }
}

# 3. Внедрение кастомного CSS для имитации дизайна макета
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #4A4543 !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    .metric-card {
        background-color: #F8F9FA;
        border: 1px solid #E9ECEF;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.02);
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 13px;
        color: #6C757D;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 26px;
        color: #212529;
        font-weight: 700;
    }
    .metric-footer {
        font-size: 11px;
        color: #28A745;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ================= БОКОВОЕ МЕНЮ (SIDEBAR) =================
st.sidebar.markdown("<h2 style='text-align: center; margin-bottom: 0;'>⚙️ Stock+</h2>", unsafe_allow_html=True)

# Переключатель языка (Является главным элементом управления локализацией)
lang_choice = st.sidebar.selectbox("🌐 Language / Язык", ["EN", "RU"])
txt = LANGUAGES[lang_choice] # Переменная txt теперь хранит все строки на выбранном языке

st.sidebar.markdown(f"<p style='text-align: center; font-size: 12px; opacity: 0.8;'>{txt['slogan']}</p>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Список разделов с иконками
menu_choice = st.sidebar.radio(
    txt["nav_title"], 
    ["📈 Dashboard", "📦 Products", "🛒 Orders", "📊 Analytics", "🗂️ Reports"]
)

st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown(txt["user_role"], unsafe_allow_html=True)

# Загрузка данных из JSON
data = load_data()
products_dict = data.get("products", {})

if products_dict:
    df_products = pd.DataFrame.from_dict(products_dict, orient='index').reset_index()
    df_products.rename(columns={'index': 'Артикул'}, inplace=True)
else:
    df_products = pd.DataFrame(columns=['Артикул', 'name', 'stock', 'purchase_price', 'selling_price'])


# ================= СЦЕНАРИИ НАВИГАЦИИ =================

# 1. DASHBOARD
if menu_choice == "📈 Dashboard":
    st.markdown("<h1 style='color: #212529;'>📈 Dashboard</h1>", unsafe_allow_html=True)
    st.caption(txt["caption_dash"])
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_items = int(df_products['stock'].sum()) if not df_products.empty else 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">📋 {txt['card_capacity']}</div>
                <div class="metric-value">{total_items} <span style="font-size: 14px; font-weight: normal; color: #6C757D;">pcs</span></div>
                <div class="metric-footer">{txt['card_capacity_foot']}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        orders_today = len(data.get("orders", []))
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">📦 {txt['card_orders']}</div>
                <div class="metric-value">{orders_today}</div>
                <div class="metric-footer">{txt['card_orders_foot']}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        low_stock_df = df_products[df_products['stock'] < 5] if not df_products.empty else pd.DataFrame()
        low_stock_count = len(low_stock_df)
        color = "#DC3545" if low_stock_count > 0 else "#212529"
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">⚠️ {txt['card_alert']}</div>
                <div class="metric-value" style="color: {color};">{low_stock_count}</div>
                <div class="metric-footer" style="color: {color};">{txt['card_alert_foot']}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        total_revenue = sum(order["total_sale"] for order in data.get("orders", []))
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">💰 {txt['card_revenue']}</div>
                <div class="metric-value">{total_revenue:,.2f} 〒</div>
                <div class="metric-footer">{txt['card_revenue_foot']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    chart_col, alert_col = st.columns([2, 1])
    
    with chart_col:
        st.markdown(f"<h5 style='color: #4A4543;'>📉 {txt['chart_title']}</h5>", unsafe_allow_html=True)
        if not df_products.empty:
            fig = px.area(
                df_products, x="name", y="stock", 
                labels={"stock": txt["chart_y"], "name": txt["chart_x"]},
                color_discrete_sequence=['#4A4543']
            )
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(txt["chart_info"])
            
    with alert_col:
        st.markdown(f"<h5 style='color: #4A4543;'>{txt['log_title']}</h5>", unsafe_allow_html=True)
        if low_stock_count > 0:
            for _, row in low_stock_df.iterrows():
                st.error(txt["log_critical"].format(row['name'], row['stock']))
        else:
            st.success(txt["log_ok"])

# 2. PRODUCTS
elif menu_choice == "📦 Products":
    st.markdown(f"<h1 style='color: #212529;'>{txt['prod_title']}</h1>", unsafe_allow_html=True)
    st.caption(txt["prod_caption"])
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander(txt["prod_expander"]):
        with st.form("new_product_form"):
            c1, c2 = st.columns(2)
            with c1:
                art = st.text_input(txt["lbl_art"])
                name = st.text_input(txt["lbl_name"])
            with c2:
                stock = st.number_input(txt["lbl_stock"], min_value=0, step=1, value=25)
                p_price = st.number_input(txt["lbl_p_price"], min_value=0.0, step=0.01)
                s_price = st.number_input(txt["lbl_s_price"], min_value=0.0, step=0.01)
            
            submit = st.form_submit_button(txt["btn_save"])
            if submit:
                if art.strip() and name.strip():
                    if add_product(art, name, stock, p_price, s_price):
                        st.success(txt["msg_success_add"].format(name))
                        st.rerun()
                else:
                    st.error(txt["msg_error_add"])
                    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### {txt['tbl_title']}")
    
    if not df_products.empty:
        df_display = df_products.copy()
        df_display.columns = [txt["col_art"], txt["col_name"], txt["col_stock"], txt["col_p_price"], txt["col_s_price"]]
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.warning(txt["tbl_empty"])

# 3. ORDERS
elif menu_choice == "🛒 Orders":
    st.markdown(f"<h1 style='color: #212529;'>{txt['ord_title']}</h1>", unsafe_allow_html=True)
    st.caption(txt["ord_caption"])
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not df_products.empty:
        with st.form("sale_form"):
            product_map = {row['name']: row['Артикул'] for _, row in df_products.iterrows()}
            selected_name = st.selectbox(txt["ord_select"], list(product_map.keys()))
            target_art = product_map[selected_name]
            
            current_available = df_products[df_products['Артикул'] == target_art]['stock'].values[0]
            st.info(txt["ord_available"].format(current_available))
            
            qty = st.number_input(txt["ord_qty"], min_value=1, max_value=int(current_available) if current_available > 0 else 1, step=1)
            
            execute_sale = st.form_submit_button(txt["ord_btn"])
            if execute_sale:
                if current_available >= qty:
                    if register_sale(target_art, qty):
                        st.success(txt["ord_success"].format(qty, selected_name))
                        st.rerun()
                else:
                    st.error(txt["ord_error"])
    else:
        st.warning(txt["ord_empty"])

# 4. ANALYTICS
elif menu_choice == "📊 Analytics":
    st.markdown(f"<h1 style='color: #212529;'>{txt['an_title']}</h1>", unsafe_allow_html=True)
    st.caption(txt["an_caption"])
    st.markdown("<br>", unsafe_allow_html=True)
    
    orders_list = data.get("orders", [])
    if orders_list:
        df_orders = pd.DataFrame(orders_list)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"#### 🍩 {txt['an_pie']}")
            fig_rev = px.pie(df_orders, names="product_name", values="total_sale", hole=0.4, color_discrete_sequence=px.colors.sequential.Gray)
            st.plotly_chart(fig_rev, use_container_width=True)
        with c2:
            st.markdown(f"#### 📈 {txt['an_bar']}")
            fig_prof = px.bar(df_orders, x="product_name", y="profit", color_discrete_sequence=['#5A5553'])
            st.plotly_chart(fig_prof, use_container_width=True)
            
        st.markdown(f"### {txt['an_log']}")
        st.dataframe(df_orders, use_container_width=True, hide_index=True)
    else:
        st.info(txt["an_empty"])

# 5. REPORTS
elif menu_choice == "🗂️ Reports":
    st.markdown(f"<h1 style='color: #212529;'>{txt['rep_title']}</h1>", unsafe_allow_html=True)
    st.caption(txt["rep_caption"])
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not df_products.empty:
        st.success(txt["rep_success"])
        df_display = df_products.copy()
        df_display.columns = [txt["col_art"], txt["col_name"], txt["col_stock"], txt["col_p_price"], txt["col_s_price"]]
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        csv_data = df_products.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=txt["rep_btn"],
            data=csv_data,
            file_name="stock_plus_report.csv",
            mime="text/csv"
        )
    else:
        st.warning(txt["rep_empty"])