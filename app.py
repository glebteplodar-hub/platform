import html

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Бизнес-Платформа",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# ДАННЫЕ (позже легко заменить на БД / API)
# ──────────────────────────────────────────────────────────────
MENU = [
    # (ключ страницы, иконка, название, бейдж)
    ("home", "🏠", "Главная", None),
    ("requests", "🎯", "Мои запросы", None),
    ("contacts", "👥", "Мои контакты", None),
    ("value", "📈", "Моя ценность", None),
    ("community", "🤝", "Сообщество", None),
    ("opportunities", "💡", "Возможности", None),
    ("messages", "✉️", "Сообщения", None),
    ("calendar", "📅", "Календарь", None),
]
PAGE_KEYS = [m[0] for m in MENU]

ACTIVITY: list[dict] = []

MEETINGS: list[dict] = []

CONTACTS = pd.DataFrame(columns=["Имя", "Роль", "Страна", "Статус"])


# ──────────────────────────────────────────────────────────────
# СОСТОЯНИЕ
# ──────────────────────────────────────────────────────────────
def init_state() -> None:
    if "user" not in st.session_state:
        st.session_state.user = None
    if "page" not in st.session_state:
        page = st.query_params.get("page", "home")
        st.session_state.page = page if page in PAGE_KEYS else "home"
    if "requests" not in st.session_state:
        st.session_state.requests = []


def go(page: str) -> None:
    """Callback кнопки меню: меняет страницу и запоминает её в URL."""
    st.session_state.page = page
    st.query_params["page"] = page


# ──────────────────────────────────────────────────────────────
# СТИЛИ
# ──────────────────────────────────────────────────────────────
CSS = """
<style>
/* Прячем только лишнее. stToolbar НЕ трогаем: в нём кнопка открытия панели */
#MainMenu, footer {visibility: hidden;}
[data-testid="stAppDeployButton"],
[data-testid="stMainMenu"],
[data-testid="stDecoration"] {display: none;}
header[data-testid="stHeader"] {background: transparent;}

/* На компьютере панель всегда открыта и не сворачивается */
@media (min-width: 993px) {
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stExpandSidebarButton"] {display: none;}
    [data-testid="stSidebar"] {
        transform: none !important;
        margin-left: 0 !important;
        min-width: 300px;
    }
}

/* Боковая панель */
[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E2E8F0;
}
[data-testid="stSidebar"] .block-container {padding-top: 1rem;}

/* Пункты меню = кнопки, выглядящие как пункты меню */
[data-testid="stSidebar"] .stButton {margin-bottom: 2px;}
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    justify-content: flex-start;
    text-align: left;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 0.9rem;
    background: transparent;
    color: #1E293B;
    font-weight: 600;
    box-shadow: none;
    transition: background-color .15s;
}
[data-testid="stSidebar"] .stButton > button p {font-size: 17px; text-align: left;}
[data-testid="stSidebar"] .stButton > button:hover {background: #F1F5F9; color: #1E293B;}
[data-testid="stSidebar"] .stButton > button:focus-visible {outline: 2px solid #4F46E5;}

/* Активный пункт (type="primary") */
[data-testid="stSidebar"] .stButton > button[kind="primary"],
[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] {
    background: #EEF2FF;
    color: #4F46E5;
    font-weight: 700;
}

/* Основной контент */
.block-container {padding-top: 2rem; max-width: 1400px;}

/* Карточки (st.container(border=True)) */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.profile-block {border-left: 2px solid #E2E8F0; padding-left: 20px; text-align: right;}

.activity-row {
    display: flex; justify-content: space-between; align-items: center; gap: 12px;
    padding: 14px 16px; margin-bottom: 8px;
    background: #FCFDFE; border: 1px solid #F1F5F9; border-radius: 8px;
}
.activity-time {color: #94A3B8; font-size: 13px; min-width: 90px;}
.activity-main {display: flex; gap: 12px; align-items: flex-start;}
.activity-sub {color: #64748B; font-size: 13px;}
.pill {padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; white-space: nowrap;}

.item-card {
    display: flex; justify-content: space-between; align-items: center; gap: 12px;
    padding: 12px 14px; margin-bottom: 8px;
    background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px;
}
.item-sub {color: #94A3B8; font-size: 12px;}
.status-ok {color: #137333; font-size: 13px; font-weight: 600; white-space: nowrap;}
</style>
"""


def e(value) -> str:
    """Экранируем всё, что попадает в HTML (защита от XSS и поломки разметки)."""
    return html.escape(str(value))


# ──────────────────────────────────────────────────────────────
# БОКОВАЯ ПАНЕЛЬ
# ──────────────────────────────────────────────────────────────
def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            "<h1 style='color:#1E3A8A;font-weight:800;font-size:30px;margin:0;'>🏛️ PLATFORM</h1>"
            "<p style='color:#64748B;font-size:14px;margin:0 0 12px 0;'>Corporate Ecosystem</p>",
            unsafe_allow_html=True,
        )
        st.divider()

        for key, icon, title, badge in MENU:
            label = f"{icon}  {title}" + (f"   ({badge})" if badge else "")
            st.button(
                label,
                key=f"nav_{key}",
                type="primary" if st.session_state.page == key else "secondary",
                on_click=go,
                args=(key,),
            )

        st.divider()
        st.markdown(
            "<div style='background:#F8FAFC;border:1px solid #E2E8F0;padding:14px;border-radius:12px;'>"
            "<p style='margin:0;font-weight:700;font-size:15px;color:#1E293B;'>🤖 Модуль AI-ассистента</p>"
            "<p style='margin:4px 0 0 0;color:#10B981;font-size:13px;font-weight:600;'>● Статус: подключён</p>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.write("")
        st.button("🚪  Выйти", key="logout", on_click=logout)


# ──────────────────────────────────────────────────────────────
# ОБЩИЕ БЛОКИ
# ──────────────────────────────────────────────────────────────
def page_header(title: str, subtitle: str, show_profile: bool = True) -> None:
    left, right = st.columns([3, 1])
    with left:
        st.markdown(
            f"<h1 style='color:#0F172A;font-weight:700;margin-bottom:5px;'>{e(title)}</h1>"
            f"<p style='color:#475569;font-size:15px;'>{e(subtitle)}</p>",
            unsafe_allow_html=True,
        )
    if show_profile:
        with right:
            st.markdown(
                "<div class='profile-block'>"
                f"<span style='font-weight:700;color:#1E293B;font-size:16px;'>{e(st.session_state.user)} 👤</span>"
                "</div>",
                unsafe_allow_html=True,
            )


def activity_row(a: dict) -> str:
    return (
        "<div class='activity-row'>"
        "<div class='activity-main'>"
        f"<span class='activity-time'>{e(a['time'])}</span>"
        f"<div>{e(a['icon'])} <b>{e(a['title'])}</b><br>"
        f"<span class='activity-sub'>{e(a['text'])}</span></div>"
        "</div>"
        f"<div class='pill' style='background:{a['bg']};color:{a['fg']};'>{e(a['badge'])}</div>"
        "</div>"
    )


def request_card(r: dict) -> str:
    sub = ""
    if r["candidates"] is not None:
        sub = f"<br><span class='item-sub'>{r['candidates']} кандидатов</span>"
    return (
        "<div class='item-card'>"
        f"<div>🎯 <b>{e(r['title'])}</b>{sub}</div>"
        "<div class='status-ok'>● В работе</div>"
        "</div>"
    )


def meeting_card(m: dict) -> str:
    return (
        "<div class='item-card'>"
        f"<div>📅 <b>{e(m['title'])}</b><br><span class='item-sub'>{e(m['where'])}</span></div>"
        f"<div style='color:#475569;font-size:12px;font-weight:700;'>{e(m['time'])}</div>"
        "</div>"
    )


def render_requests() -> None:
    if st.session_state.requests:
        st.markdown("".join(request_card(r) for r in st.session_state.requests), unsafe_allow_html=True)
    else:
        st.caption("Запросов пока нет.")


def render_meetings() -> None:
    if MEETINGS:
        st.markdown("".join(meeting_card(m) for m in MEETINGS), unsafe_allow_html=True)
    else:
        st.caption("Встреч пока нет.")


# ──────────────────────────────────────────────────────────────
# СТРАНИЦЫ
# ──────────────────────────────────────────────────────────────
def page_home() -> None:
    page_header("Панель управления активами", "Сводный аналитический отчёт по вашей бизнес-активности.")
    st.write("")

    requests_count = len(st.session_state.requests)
    metrics = [
        ("💼 Активные деловые запросы", str(requests_count), "0 в обработке"),
        ("🤝 Подтверждённые контакты", "0", "0 новых партнёров"),
        ("📊 Ценность активов", "€0", "0,0% изменений"),
    ]
    for col, (label, value, delta) in zip(st.columns(3), metrics):
        with col, st.container(border=True):
            st.metric(label=label, value=value, delta=delta, delta_color="off")

    st.write("")
    st.subheader("KPI и индексы эффективности")
    kpis = [
        ("🛡️ Индекс надёжности", "0 / 100", "Требуется верификация"),
        ("⭐ Корпоративные баллы", "0", "Нет активных сессий"),
        ("🏢 Привлечённые компании", "0 организаций", "Ожидание"),
        ("📢 Внешние рекомендации", "0 полученных", "За период"),
    ]
    for col, (title, value, note) in zip(st.columns(4), kpis):
        with col:
            st.info(f"**{title}**\n\n**{value}**\n\n{note}")

    st.divider()

    left, right = st.columns([1.6, 1.0])

    with left:
        st.subheader("⏳ Недавняя активность")
        tabs = st.tabs(["Все", "Запросы", "Контакты", "Сделки", "Возможности", "Достижения"])
        kinds = [None, "requests", "contacts", "deals", "opportunities", "achievements"]
        for tab, kind in zip(tabs, kinds):
            with tab:
                rows = [a for a in ACTIVITY if kind is None or a["kind"] == kind]
                if rows:
                    st.markdown("".join(activity_row(a) for a in rows), unsafe_allow_html=True)
                else:
                    st.caption("Здесь пока пусто.")

    with right:
        st.subheader("📊 Текущие запросы")
        render_requests()
        st.button("Все запросы", on_click=go, args=("requests",), key="home_all_requests")

        st.subheader("📅 Ближайшие встречи")
        render_meetings()
        st.button("Открыть календарь", on_click=go, args=("calendar",), key="home_calendar")


def page_requests() -> None:
    page_header("Мои запросы", "Создавайте и отслеживайте деловые запросы.")
    with st.form("new_request", clear_on_submit=True):
        title = st.text_input("Что вы ищете?", placeholder="Например: поставщик светодиодных панелей")
        if st.form_submit_button("Создать запрос", type="primary"):
            title = title.strip()
            if not title:
                st.error("Введите название запроса.")
            else:
                st.session_state.requests.append({"title": title, "candidates": 0})
                st.success("Запрос создан.")

    render_requests()


def page_contacts() -> None:
    page_header("Мои контакты", "Люди и компании из вашей сети.")
    query = st.text_input("Поиск", placeholder="Имя, роль или страна", label_visibility="collapsed")
    df = CONTACTS
    if query and not df.empty:
        mask = df.apply(lambda col: col.astype(str).str.contains(query, case=False, regex=False)).any(axis=1)
        df = df[mask]
    if CONTACTS.empty:
        st.caption("У вас пока нет контактов.")
    elif df.empty:
        st.caption("Ничего не найдено. Попробуйте другой запрос.")
    else:
        st.dataframe(df, hide_index=True, use_container_width=True)


def page_messages() -> None:
    page_header("Сообщения", "Входящие сообщения и уведомления.")
    st.info("Новых сообщений нет.")


def page_calendar() -> None:
    page_header("Календарь", "Ближайшие встречи и события.")
    render_meetings()


def page_stub(title: str, subtitle: str):
    def _render() -> None:
        page_header(title, subtitle)
        st.info("Раздел в разработке.")
    return _render


PAGES = {
    "home": page_home,
    "requests": page_requests,
    "contacts": page_contacts,
    "value": page_stub("Моя ценность", "Оценка ваших активов и вклада."),
    "community": page_stub("Сообщество", "Профессиональные группы и обсуждения."),
    "opportunities": page_stub("Возможности", "Подборка предложений под ваши запросы."),
    "messages": page_messages,
    "calendar": page_calendar,
}


# ──────────────────────────────────────────────────────────────
# ЭКРАН ВХОДА
# ──────────────────────────────────────────────────────────────
def logout() -> None:
    st.session_state.user = None


def render_login() -> None:
    # На экране входа боковая панель не нужна
    st.markdown(
        "<style>[data-testid='stSidebar'], [data-testid='stSidebarCollapsedControl'], "
        "[data-testid='stExpandSidebarButton'] {display: none !important;}</style>",
        unsafe_allow_html=True,
    )
    _, center, _ = st.columns([1, 1.2, 1])
    with center:
        st.write("")
        st.write("")
        st.markdown(
            "<h1 style='color:#1E3A8A;font-weight:800;font-size:34px;margin:0;'>🏛️ PLATFORM</h1>"
            "<p style='color:#64748B;font-size:14px;margin:0 0 16px 0;'>Corporate Ecosystem</p>",
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            st.subheader("Добро пожаловать")
            st.caption("Введите имя и фамилию, чтобы продолжить.")
            with st.form("login"):
                first = st.text_input("Имя", max_chars=40)
                last = st.text_input("Фамилия", max_chars=40)
                if st.form_submit_button("Войти", type="primary"):
                    first, last = first.strip(), last.strip()
                    if not first or not last:
                        st.error("Введите и имя, и фамилию.")
                    else:
                        st.session_state.user = f"{first} {last}"
                        st.rerun()


# ──────────────────────────────────────────────────────────────
# ЗАПУСК
# ──────────────────────────────────────────────────────────────
st.markdown(CSS, unsafe_allow_html=True)
init_state()
if not st.session_state.user:
    render_login()
    st.stop()
render_sidebar()
PAGES[st.session_state.page]()
