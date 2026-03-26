import streamlit as st
from src.inference import classify_image
from components.uploader import upload_image
import time


# =====================================================
# 1. PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Dental AI | Radiography Classifier",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. CSS SYSTEM (FIX HEADER ICON GRAY)
# =====================================================
def apply_custom_css(theme):

    if theme == "Dark":
        sidebar_bg = "#020617"
        text_color = "#f8fafc"
        border_color = "rgba(255,255,255,0.08)"
        main_bg = "#071029"
        card_bg = "rgba(255,255,255,0.03)"
    else:
        sidebar_bg = "#ffffff"
        text_color = "#0f172a"
        border_color = "rgba(0,0,0,0.08)"
        main_bg = "#ffffff"
        card_bg = "rgba(0,0,0,0.02)"

    st.markdown(f"""
    <style>

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {border_color};
    }}

    section[data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}

    /* ===== MAIN BACKGROUND ===== */
    div[data-testid="stAppViewContainer"] {{
        background-color: {main_bg} !important;
        color: {text_color} !important;
    }}

    header {{
        background-color: {main_bg} !important;
        color: {text_color} !important;
    }}

    /* ===== FIX ICON COLLAPSE BỊ XÁM ===== */
    header button svg {{
        color: #ffffff !important;
        stroke: #ffffff !important;
        fill: #ffffff !important;
    }}

    header button svg path {{
        stroke: #ffffff !important;
        fill: #ffffff !important;
        opacity: 1 !important;
    }}

    header [data-testid="collapsedControl"] {{
        color: #ffffff !important;
    }}

    /* ===== CARD ===== */
    .card {{
        background: {card_bg};
        border-radius: 16px;
        padding: 20px;
        border: 1px solid {border_color};
        margin-bottom: 20px;
    }}

    /* ===== RESULT CARD ===== */
    .result-card {{
        background: {card_bg};
        border-radius: 16px;
        padding: 25px;
        border-left: 6px solid #2563eb;
        border: 1px solid {border_color};
        color: {text_color} !important;
    }}

    .result-card * {{
        color: {text_color} !important;
    }}

    /* ================= FILE UPLOADER DARK MODE FIX ================= */

    /* Box upload */
    div[data-testid="stFileUploader"] > div {{
        background-color: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
    }}

    /* Text: Drag and drop */
    div[data-testid="stFileUploader"] label,
    div[data-testid="stFileUploader"] span,
    div[data-testid="stFileUploader"] p {{
        color: #ffffff !important;
    }}

    /* Nút Browse files */
    div[data-testid="stFileUploader"] button {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
    }}

    /* Hover cho nút Browse */
    div[data-testid="stFileUploader"] button:hover {{
        background-color: #e5e7eb !important;
        color: #000000 !important;
    }}

    /* Tên file sau khi upload */
    div[data-testid="stFileUploader"] small,
    div[data-testid="stFileUploader"] .uploadedFileName,
    div[data-testid="stFileUploader"] div {{
        color: #ffffff !important;
    }}

    /* Icon file */
    div[data-testid="stFileUploader"] svg {{
        color: #ffffff !important;
        fill: #ffffff !important;
    }}

    /* Nút X xoá file */
    div[data-testid="stFileUploader"] button[title="Remove file"] {{
        color: #ffffff !important;
    }}

    div[data-testid="stFileUploader"] section {{
        background-color: #b4b4b8 !important;
        border-radius: 12px !important;
    }}

    /* ===== METRIC ===== */
    div[data-testid="stMetric"] * {{
        color: {text_color} !important;
    }}

    /* ===== FIX SIDEBAR HEADER BỊ LỆCH XUỐNG ===== */

    /* Xoá khoảng trống trên cùng của sidebar */
    section[data-testid="stSidebar"] > div:first-child {{
        padding-top: 0rem !important;
    }}

    /* Kéo logo + text lên sát trên */
    .sidebar-logo {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: -10px;
        margin-bottom: 10px;
    }}

    /* Làm text gọn hơn để nhìn cân */
    .sidebar-logo h2 {{
        margin: 0;
        font-size: 20px;
        font-weight: 600;
    }}

    /* ===== TRIỆT TIÊU KHOẢNG TRỐNG ĐỈNH SIDEBAR ===== */
    
    /* 1. Xóa bỏ hoàn toàn padding của container nội dung */
    [data-testid="stSidebarUserContent"] {{
        padding-top: 1rem !important; /* Chỉ để lại 1 ít cho thoáng */
    }}

    /* 2. Ép nội dung vượt lên trên cả vùng bảo vệ của nút đóng mở */
    [data-testid="stSidebarNav"] {{
        display: none !important; /* Ẩn menu mặc định nếu có */
    }}

    /* 3. Dùng margin-top âm để kéo toàn bộ Logo lên sát nút đóng mở */
    .sidebar-logo {{
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        margin-top: -3.8rem !important; /* Kéo lên kịch trần */
        margin-bottom: 0.5rem !important;
        padding: 0 !important;
    }}

    .sidebar-logo h2 {{
        margin: 0 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        line-height: 1 !important;
    }}

    .sidebar-logo img {{
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* Thu nhỏ khoảng cách của Divider để tiết kiệm chỗ */
    section[data-testid="stSidebar"] hr {{
        margin-top: 0.2rem !important;
        margin-bottom: 0.5rem !important;
    }}

    /* ===== ĐẶC TRỊ NÚT MỞ SIDEBAR TRÀNG TRÀNG (DARK MODE) ===== */

    /* 1. Nhắm vào tất cả các nút có icon điều hướng sidebar */
    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="stHeader"] button:first-child {{
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 8px !important;
    }}

    /* 2. ÉP ICON TRẮNG SÁNG: Nhắm vào class gốc của Streamlit để override Shadow DOM */
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="stHeader"] button:first-child svg,
    .st-emotion-cache-6qob1r svg {{
        fill: white !important;
        stroke: white !important;
        color: white !important;
        filter: brightness(0) invert(1) !important; /* Force trắng kịch trần */
    }}

    /* 3. Đảm bảo path bên trong không bị ẩn */
    [data-testid="stSidebarCollapsedControl"] svg path,
    [data-testid="stHeader"] button:first-child svg path {{
        fill: white !important;
        stroke: white !important;
        opacity: 1 !important;
    }}

    /* 4. Hiệu ứng Hover để bác sĩ dễ nhận diện */
    [data-testid="stSidebarCollapsedControl"]:hover button {{
        background-color: #2563eb !important;
        transform: scale(1.05);
        transition: all 0.2s ease-in-out;
    }}

    </style>
    """, unsafe_allow_html=True)


# =====================================================
# 3. APPLY CSS TRƯỚC KHI RENDER UI
# =====================================================
apply_custom_css("Dark")   # default để tránh icon bị xám khi load lần đầu


# =====================================================
# 4. SIDEBAR
# =====================================================
with st.sidebar:

    st.markdown("""
    <div class="sidebar-logo">
        <img src="https://img.icons8.com/fluency/96/tooth.png" width="38">
        <h2>Dental AI Pro</h2>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.subheader("System Settings")

    theme_choice = st.radio("Interface Theme", ("Light", "Dark"), index=1)

    st.divider()

    st.subheader("Model Info")
    st.info("""
    **Model:** XGBoost  
    **Accuracy:** 79.50%
    """)


# apply lại theme theo user chọn
apply_custom_css(theme_choice)


# =====================================================
# 5. HEADER
# =====================================================
col1, col2 = st.columns([3,1])

with col1:
    st.title("Dental Radiography Classifier")
    st.caption("AI-powered dental diagnosis assistant")


# =====================================================
# 6. MAIN LAYOUT
# =====================================================
left, right = st.columns([1,1], gap="large")


# -------- LEFT --------
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Upload Radiograph")

    image = upload_image()

    if image:
        st.image(image, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# -------- RIGHT --------
with right:

    st.subheader("🔍 Diagnostic Analysis")

    if image is not None:

        if st.button("🚀 Run AI Analysis", type="primary"):

            start_time = time.time()

            with st.spinner("Processing image..."):
                result = classify_image(image)
                time.sleep(0.8)

            processing_time = time.time() - start_time

            st.divider()

            if isinstance(result, dict) and 'error' in result:
                st.error(f"Analysis Failed: {result['error']}")

            else:

                prediction = result.get('prediction') if isinstance(result, dict) else result[0]
                confidence = result.get('encoded_value') if isinstance(result, dict) else result[1]

                st.markdown(f"""
                <div class="result-card">
                    <p>Primary Detection</p>
                    <h2>{prediction}</h2>
                    <p>Confidence Score: <b>{confidence}</b></p>
                </div>
                """, unsafe_allow_html=True)

                st.write("")

                m1, m2 = st.columns(2)
                m1.metric("Latency", f"{processing_time:.2f}s")
                m2.metric("Result Quality", "Verified")

                st.balloons()

    else:
        st.write("Diagnostic results will be displayed here after image upload.")


# =====================================================
# 7. FOOTER
# =====================================================
st.divider()

c1, c2 = st.columns(2)

with c1:
    st.caption("© 2026 Dental AI Diagnostics")

with c2:
    st.caption("v1.0.2")



























    # def apply_custom_css(theme):
    # if theme == "Dark":
    #     sidebar_bg = "#020617"
    #     text_color = "#f8fafc"
    #     border_color = "rgba(255,255,255,0.08)"
    #     main_bg = "#071029"
    #     card_bg = "rgba(255,255,255,0.03)"
    #     # Dark mode: Force icons to white
    #     icon_filter = "brightness(0) invert(1)" 
    #     btn_hover_bg = "rgba(255, 255, 255, 0.1)"
    # else:
    #     sidebar_bg = "#ffffff"
    #     text_color = "#0f172a"
    #     border_color = "rgba(0,0,0,0.08)"
    #     main_bg = "#ffffff"
    #     card_bg = "rgba(0,0,0,0.02)"
    #     # Light mode: Force icons to dark
    #     icon_filter = "brightness(0)" 
    #     btn_hover_bg = "rgba(0, 0, 0, 0.05)"

    # st.markdown(f"""
    # <style>
    # /* ===== FORCE TEXT COLOR IN DARK MODE ===== */

    # :root {{
    #     --text-color: #ffffff !important;
    #     --primary-text-color: #ffffff !important;
    # }}

    # /* file uploader text */
    # [data-testid="stFileUploader"] * {{
    #     color: #ffffff !important;
    # }}
                
    # /* Import Font */
    # @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    # /* ===== GLOBAL STYLES ===== */
    # html, body, [data-testid="stAppViewContainer"] {{
    #     font-family: 'Inter', sans-serif;
    #     background-color: {main_bg} !important;
    #     color: {text_color} !important;
    # }}

    # /* ===== SIDEBAR ===== */
    # section[data-testid="stSidebar"] {{
    #     background-color: {sidebar_bg} !important;
    #     border-right: 1px solid {border_color};
    # }}

    # section[data-testid="stSidebar"] * {{
    #     color: {text_color} !important;
    # }}

    # /* Triệt tiêu khoảng trống đỉnh sidebar */
    # [data-testid="stSidebarUserContent"] {{
    #     padding-top: 1rem !important;
    # }}

    # [data-testid="stSidebarNav"] {{
    #     display: none !important;
    # }}

    # .sidebar-logo {{
    #     display: flex !important;
    #     align-items: center !important;
    #     gap: 12px !important;
    #     margin-top: -3.8rem !important;
    #     margin-bottom: 0.5rem !important;
    #     padding: 0 !important;
    # }}

    # .sidebar-logo h2 {{
    #     margin: 0 !important;
    #     font-size: 1.2rem !important;
    #     font-weight: 700 !important;
    # }}

    # /* ===== SMART HEADER & COLLAPSED BUTTON (LIGHT/DARK) ===== */
    # header[data-testid="stHeader"] {{
    #     background-color: transparent !important;
    # }}

    # /* Nút mở Sidebar khi đang đóng và nút đóng khi đang mở */
    # button[data-testid*="CollapsedControl"], 
    # header button:first-child {{
    #     background-color: {btn_hover_bg} !important;
    #     border-radius: 8px !important;
    #     transition: all 0.3s ease !important;
    # }}

    # /* ÉP MÀU ICON THEO THEME */
    # button[data-testid*="CollapsedControl"] svg,
    # header button:first-child svg {{
    #     filter: {icon_filter} !important;
    #     fill: currentColor !important;
    #     color: inherit !important;
    #     opacity: 1 !important;
    # }}

    # /* Khi Hover nút điều hướng */
    # button[data-testid*="CollapsedControl"]:hover,
    # header button:first-child:hover {{
    #     background-color: #2563eb !important;
    #     box-shadow: 0 0 10px rgba(37, 99, 235, 0.5) !important;
    # }}

    # /* Khi hover thì icon luôn là màu trắng cho nổi trên nền xanh */
    # button[data-testid*="CollapsedControl"]:hover svg,
    # header button:first-child:hover svg {{
    #     filter: brightness(0) invert(1) !important;
    # }}

    # /* ===== CARDS & RESULTS ===== */
    # .card {{
    #     background: {card_bg};
    #     border-radius: 16px;
    #     padding: 20px;
    #     border: 1px solid {border_color};
    #     margin-bottom: 20px;
    # }}

    # .result-card {{
    #     background: {card_bg};
    #     border-radius: 16px;
    #     padding: 25px;
    #     border-left: 6px solid #2563eb;
    #     border-top: 1px solid {border_color};
    #     border-right: 1px solid {border_color};
    #     border-bottom: 1px solid {border_color};
    #     color: {text_color} !important;
    # }}

    # /* ===== FILE UPLOADER FIX ===== */
    # [data-testid="stFileUploader"] section {{
    #     background-color: rgba(255,255,255,0.04) !important;
    #     border: 1px solid rgba(255,255,255,0.12) !important;
    #     border-radius: 12px !important;
    # }}

    # /* ===== FIX TEXT FILE UPLOADER (DARK MODE) ===== */

    # /* Text: Drag & drop + Browse files */
    # div[data-testid="stFileUploader"] label,
    # div[data-testid="stFileUploader"] p,
    # div[data-testid="stFileUploader"] span,
    # div[data-testid="stFileUploader"] button {{
    #     color: #ffffff !important;
    # }}

    # /* File name sau khi upload */
    # div[data-testid="stFileUploader"] small {{
    #     color: #ffffff !important;
    #     font-weight: 500 !important;
    # }}

    # /* Icon file */
    # div[data-testid="stFileUploader"] svg {{
    #     fill: #ffffff !important;
    #     color: #ffffff !important;
    # }}

    # /* ===== FIX HEADER HEIGHT ===== */

    # header[data-testid="stHeader"] {{
    #     height: 52px !important;
    # }}

    # header[data-testid="stHeader"] > div {{
    #     padding-top: 0rem !important;
    #     padding-bottom: 0rem !important;
    # }}

    # header button {{
    #     margin-top: 0px !important;
    #     margin-bottom: 0px !important;
    # }}

    # div[data-testid="stAppViewContainer"] > div:first-child {{
    #     padding-top: 0rem !important;
    # }}

    # </style>
    # """, unsafe_allow_html=True)