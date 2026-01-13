import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Loan Chain",
    page_icon="💸",
    layout="wide"
)

with st.sidebar:
    st.sidebar.image(
        "https://i.imgur.com/Rd8GyFU.png",
        use_container_width=True
    )
    st.sidebar.markdown("📘 **About**")
    st.sidebar.markdown("""
    **Loan Chain** is the shared control plane for syndicated loan risk, where every party sees the same truth, at the same time
    
    ---
    #### 🔮 Vision Statement
    
    Designed to help agent banks keep syndicated loans on track throughout their lifecycle by providing real-time transparency, proactive risk monitoring, and blockchain-verified records accessible to all syndicate members simultaneously.
   
    ---
    ### 🧩 Apps Showcase
    Our apps and tools can be seen here:
    [ELPEEF](https://showcase.elpeef.com/)
    
    ---
    #### 🙌 Support & Contribute
    
    - ⭐ **Star / Fork**: [GitHub repo](https://github.com/mrbrightsides/loanchain)
    - Built with 💙 by [Khudri](https://s.id/khudri)
    - Dukung pengembangan proyek ini melalui: 
      [💖 GitHub Sponsors](https://github.com/sponsors/mrbrightsides) • 
      [☕ Ko-fi](https://ko-fi.com/khudri) • 
      [💵 PayPal](https://www.paypal.com/paypalme/akhmadkhudri) • 
      [🍵 Trakteer](https://trakteer.id/akhmad_khudri)

    Versi UI: v1.0 • Streamlit • Theme Dark
    """)

def embed_iframe(src, height=900):
    components.html(f"""
    <div style="width:100%; height:{height}px;">
        <iframe src="{src}"
                style="width:100%; height:100%; border:none; border-radius:12px;">
        </iframe>
    </div>
    """, height=height)

iframe_url = "https://loanchain.elpeef.com/"

embed_iframe(iframe_url, height=900)
