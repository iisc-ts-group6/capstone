import React, { useEffect, useRef, useState } from 'react';
import { BioLearn_logo } from '../assets';
import gsap from 'gsap';

const MainContent = () => {
    const questionsData = [
        {
            "id": 1,
            "question": "What is photosynthesis?",
            "answer": "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to create oxygen and energy in the form of sugar."
        },
        {
            "id": 2,
            "question": "What is the function of the nucleus in a cell?",
            "answer": "The nucleus controls the cell's activities and contains the cell's genetic material, DNA."
        },
        {
            "id": 3,
            "question": "What is the process by which cells convert glucose into usable energy?",
            "answer": "Cellular respiration is the process by which cells convert glucose and oxygen into usable energy, carbon dioxide, and water."
        },
        {
            "id": 4,
            "question": "What are enzymes and what role do they play in biological reactions?",
            "answer": "Enzymes are biological molecules that act as catalysts, speeding up chemical reactions in living organisms. They lower the activation energy required for reactions to occur, allowing them to proceed more quickly."
        },
        {
            "id": 5,
            "question": "What is the structure and function of chloroplasts?",
            "answer": "Chloroplasts are organelles found in plant cells that are responsible for photosynthesis. They contain chlorophyll, a green pigment that captures sunlight, and other molecules necessary for the conversion of light energy into chemical energy."
        }
    ];

    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [userAnswer, setUserAnswer] = useState('');
    const [isAnswerSubmitted, setIsAnswerSubmitted] = useState(false);
    const [isAnswerCorrect, setIsAnswerCorrect] = useState(false);
    const [showFeedback, setShowFeedback] = useState(false);

    const responseRef = useRef(null);

    const handleSubmit = (e) => {
        e.preventDefault();
        const correctAnswer = questionsData[currentQuestionIndex].answer;
        const isCorrect = userAnswer.trim().toLowerCase() === correctAnswer.toLowerCase();
        setIsAnswerCorrect(isCorrect);
        setIsAnswerSubmitted(true);
        setShowFeedback(true);
    }

    const handleNextQuestion = () => {
        setUserAnswer('');
        setIsAnswerSubmitted(false);
        setIsAnswerCorrect(false);
        setShowFeedback(false);
        setCurrentQuestionIndex((prevIndex) => (prevIndex + 1) % questionsData.length);
    }

    useEffect(() => {
        if (isAnswerSubmitted && showFeedback) {
            const timeline = gsap.timeline();
            timeline.fromTo(responseRef.current, { opacity: 0, y: -50, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: 'power1.inOut' })
                .fromTo('#text', { opacity: 0, y: -20 }, { opacity: 1, y: 0, ease: 'power1.inOut' }, "-=0.3")
                .fromTo('.para', { opacity: 0, y: -20 }, { opacity: 1, y: 0, delay: 0.5, stagger: 0.3 }, "-=0.3");
        }
    }, [isAnswerSubmitted, showFeedback]);

    const currentQuestion = questionsData[currentQuestionIndex];

    return (
        <div className="w-full mt-32 sm:mt-24 lg:mt-20 lg:w-5/6 flex justify-center items-center mx-auto py-8 p-4 md:p-8">
            <div className="w-full h-auto bg-white text-black rounded-xl">
                {/* Header */}
                <div className='border-b-2'>
                    <div className="m-4 flex items-center">
                        <img className="w-6 h-6 object-cover" src={BioLearn_logo} alt="Logo" />
                        <span className="font-bold ml-4 text-3xl">Question {currentQuestion.id}</span>
                    </div>
                </div>

                <section className={`${!isAnswerSubmitted ? 'block' : 'hidden'} m-4 lg:mt-10 lg:mx-20 xl:mx-40 mt-10`}>
                    <h1 className="font-bold text-xl">{currentQuestion.question}</h1>
                    <form onSubmit={handleSubmit}>
                        <textarea
                            className="w-full mt-5 p-2 px-4 border-2 border-black/20 rounded font-normal bg-none outline-none text-justify"
                            rows="8"
                            placeholder='Type your answer.'
                            value={userAnswer}
                            onChange={(e) => setUserAnswer(e.target.value)}
                            required
                        ></textarea>
                        <div className="flex justify-end my-3">
                            <button className="font-semibold bg-[#19e76f] duration-200 hover:bg-[#21b55f] p-3 px-8 lg:px-12 rounded-2xl">Submit</button>
                        </div>
                    </form>
                </section>

                {isAnswerSubmitted && (
                    <div className={`${showFeedback ? 'block' : 'hidden'} mt-10 `} ref={responseRef} id="text">
                        <div className="m-4 lg:mx-20 xl:mx-40 para">
                            <h1 className="font-semibold text-lg">
                                {isAnswerCorrect ? "Your answer is correct" : "Your answer is incorrect."}
                            </h1>
                            {!isAnswerCorrect && <p><span className='font-semibold text-md'>The right answer is:</span> {currentQuestion.answer}</p>}
                        </div>

                        <div className="m-4 lg:mx-20 xl:mx-40 mb-6 flex justify-end para">
                            <button
                                className="p-3 px-8 font-semibold duration-200 hover:bg-[#afb0b1] bg-[#e1e3e1] rounded-2xl"
                                onClick={handleNextQuestion}
                            >
                                Next Question
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default MainContent;
