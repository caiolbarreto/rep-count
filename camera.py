# streamlit_app.py
import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration, VideoTransformerBase
from pose_detection import pose_detection, Exercise


exercises = [
    Exercise(name="shoulder_press", start_angle=70, finish_angle=150),
    Exercise(name="biceps_curl", start_angle=130, finish_angle=30),
    Exercise(name="squat", start_angle=170, finish_angle=120),
]

class VideoTransformer(VideoTransformerBase):
    def _init_(self, exercise_index):
        super()._init_()
        self.exercise_index = exercise_index
        self.rep_count = 0

    def update_rep_count(self, count):
        self.rep_count = count

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        result_image, count = pose_detection(exercises[self.exercise_index], img)
        self.update_rep_count(count)
        return result_image
    
def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    if st.session_state["page"] == "Home":
        st.title("Selecione um exercício")
        exercicios_gifs = {
            "Desenvolvimento": "https://www.mundoboaforma.com.br/wp-content/uploads/2020/12/desenvolvimento-para-ombros-com-halteres.gif",
            "Rosca direta": "https://www.mundoboaforma.com.br/wp-content/uploads/2022/09/rosca-biceps-direta-com-halteres.gif",
            "Agachamento livre": "https://www.mundoboaforma.com.br/wp-content/uploads/2020/11/agachamento-livre-1.gif",
        }

        opcoes = ["Desenvolvimento", "Rosca direta", "Agachamento livre"]

        col1, col2 = st.columns(2)

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

        if option:
            if option == "Desenvolvimento":
                st.session_state["movimento"] = 0
            elif option == "Rosca direta":
                st.session_state["movimento"] = 1
            elif option == "Agachamento livre":
                st.session_state["movimento"] = 2

            button_clicked = st.button("Iniciar")

            if button_clicked:
                st.session_state["page"] = "Webcam"
                st.session_state["selected_exercise"] = option
                for exercise in exercises:
                    exercise.count = 0
                st.rerun()

    if st.session_state["page"] == "Webcam":
        st.title("Execute o seu treino!")
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
                video_transformer = VideoTransformer(exercise_index)
                webrtc_streamer(
                    key="pose-detection",
                    video_processor_factory=lambda: video_transformer,
                    rtc_configuration=RTCConfiguration(
                        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
                    ),
                    media_stream_constraints={"video": {
            "width": {"min": 1280, "ideal": 1280, "max": 1920 },
            "height": {"min": 720, "ideal": 720, "max": 1080}},
                     "audio": False},
                    desired_playing_state=True,
                )

                if st.button("Finalizar treino"):
                    st.session_state["page"] = "Conclusao"
                    st.rerun()

    if st.session_state["page"] == "Conclusao":
        st.title("Parabéns por finalizar o treinamento!")
        if st.button("Voltar ao menu"):
            st.session_state["page"] = "Home"
            st.rerun()


if _name_ == "_main_":
    main()