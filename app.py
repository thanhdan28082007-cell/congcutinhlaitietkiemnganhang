import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.caption("Tính lãi theo lãi đơn hoặc lãi kép")

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin tiền gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

loai_lai = st.selectbox(
    "Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)

st.divider()

# =========================
# NÚT TÍNH
# =========================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất theo tháng
    lai_suat_nam = lai_suat / 100
    lai_suat_thang = lai_suat_nam / 12

    # Thời gian tính theo năm
    so_nam = ky_han / 12

    # =========================
    # TÍNH LÃI ĐƠN
    # =========================
    if loai_lai == "Lãi đơn":

        tong_lai = so_tien * lai_suat_nam * so_nam

        # Lãi phát sinh mỗi tháng
        lai_thang = so_tien * lai_suat_thang

        # Lãi mỗi quý
        lai_quy = lai_thang * 3

        if hinh_thuc == "Lãnh lãi hàng tháng":
            lai_dinh_ky = lai_thang

        elif hinh_thuc == "Lãnh lãi hàng quý":
            lai_dinh_ky = lai_quy

        else:
            lai_dinh_ky = tong_lai

        tong_tien = so_tien + tong_lai

    # =========================
    # TÍNH LÃI KÉP
    # =========================
    else:

        # Lãi kép được nhập lãi vào gốc hàng tháng.
        # Công thức:
        # A = P * (1 + r/12)^n

        tong_tien = so_tien * (1 + lai_suat_thang) ** ky_han
        tong_lai = tong_tien - so_tien

        if hinh_thuc == "Lãnh lãi hàng tháng":

            # Khi lãnh lãi hàng tháng thì tiền lãi
            # không được nhập vào gốc.
            # Vì vậy thực tế khoản tiền nhận hàng tháng
            # được tính trên số tiền gốc ban đầu.
            lai_dinh_ky = so_tien * lai_suat_thang

            # Tổng tiền cuối kỳ trong trường hợp
            # lãnh lãi hàng tháng
            tong_lai = lai_dinh_ky * ky_han
            tong_tien = so_tien + tong_lai

        elif hinh_thuc == "Lãnh lãi hàng quý":

            lai_quy = so_tien * (
                (1 + lai_suat_thang) ** 3 - 1
            )

            so_quy = ky_han // 3

            # Nếu kỳ hạn không chia hết cho 3,
            # phần tháng còn lại được tính riêng.
            thang_le = ky_han % 3

            tong_lai = (
                lai_quy * so_quy
                + so_tien
                * ((1 + lai_suat_thang) ** thang_le - 1)
            )

            tong_tien = so_tien + tong_lai
            lai_dinh_ky = lai_quy

        else:
            lai_dinh_ky = tong_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("Đã tính toán thành công!")

    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tiền gửi",
            format_money(so_tien)
        )

        st.metric(
            "Tiền lãi định kỳ",
            format_money(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "Tổng tiền lãi",
            format_money(tong_lai)
        )

        st.metric(
            "Tổng gốc + lãi",
            format_money(tong_tien)
        )

    # =========================
    # THÔNG TIN CHI TIẾT
    # =========================
    st.divider()

    st.subheader("📝 Chi tiết")

    st.write(f"**Số tiền gửi:** {format_money(so_tien)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Phương pháp:** {loai_lai}")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")

    st.info(
        f"""
        **Tổng kết**

        - Tiền gốc: **{format_money(so_tien)}**
        - Tổng tiền lãi: **{format_money(tong_lai)}**
        - Tổng nhận được: **{format_money(tong_tien)}**
        """
    )

# =========================
# GHI CHÚ
# =========================
st.divider()

with st.expander("ℹ️ Ghi chú về cách tính"):
    st.write("""
    **Lãi đơn:** tiền lãi được tính dựa trên số tiền gốc ban đầu,
    không cộng lãi vào gốc.

    **Lãi kép:** tiền lãi được cộng vào tiền gốc để tiếp tục
    tính lãi cho các kỳ tiếp theo.

    Với lựa chọn **lãnh lãi hàng tháng/quý**, tiền lãi được xem
    là được trả ra ngoài và không nhập vào tiền gốc.
    """)
