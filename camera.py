# streamlit_app.py
import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
from pose_detection import pose_detection, exercises


def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    st.title("Selecione um exercício")
    if st.session_state["page"] == "Home":
        exercicios_gifs = {
            "Desenvolvimento": "https://www.mundoboaforma.com.br/wp-content/uploads/2020/12/desenvolvimento-para-ombros-com-halteres.gif",
            "Rosca direta": "https://www.mundoboaforma.com.br/wp-content/uploads/2022/09/rosca-biceps-direta-com-halteres.gif",
            "Agachamento livre": "https://www.mundoboaforma.com.br/wp-content/uploads/2020/11/agachamento-livre-1.gif",
        }

        # Opções de exercícios
        opcoes = ["Desenvolvimento", "Rosca direta", "Agachamento livre"]

        # Coluna para exibir o GIF
        col1, col2 = st.columns(2)

        # Exibe o GIF do exercício selecionado
        with col1:
            option = st.radio(
                "Opções",
                opcoes,
                key="exercicio_selecionado",
            )

        with col2:
            if option:
                st.image(exercicios_gifs[option])
                st.write(f"Exercício selecionado: {option}")

        # Direcionamento para página específica do exercício
        if option:
            if option == "Desenvolvimento":
                st.session_state["movimento"] = 0
            elif option == "Rosca direta":
                st.session_state["movimento"] = 1
            elif option == "Agachamento livre":
                st.session_state["movimento"] = 2

            # Track if the button has been clicked
            button_clicked = st.button("Iniciar")

            # Check if the button has been clicked and change page accordingly
            if button_clicked:
                st.session_state["page"] = "Webcam"
                st.session_state["selected_exercise"] = option
                st.rerun()

    if st.session_state["page"] == "Webcam":
        st.title("Clique em iniciar para começar sua sessão")
        selected_exercise = st.session_state.get("selected_exercise")
        if selected_exercise:
            exercise_index = None
            if selected_exercise == "Desenvolvimento":
                exercise_index = 0
            elif selected_exercise == "Rosca direta":
                exercise_index = 1
            elif selected_exercise == "Agachamento livre":
                exercise_index = 2

            if exercise_index is not None:
                webrtc_streamer(
                    key="pose-detection",
                    video_processor_factory=lambda: pose_detection(
                        exercises[exercise_index]
                    ),
                    rtc_configuration=RTCConfiguration(
                        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
                    ),
                    media_stream_constraints={"video": True, "audio": False},
                )
        if st.button("Voltar ao menu"):
            st.session_state["page"] = "Home"
            st.rer


if __name__ == "__main__":
    main()
