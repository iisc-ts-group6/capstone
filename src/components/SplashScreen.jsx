import React, { useEffect } from 'react';
import gsap from 'gsap';
import { TextPlugin } from 'gsap/TextPlugin';
import { microscope1, splesh_screen, splesh_screen1, splesh_screen2, splesh_screen3, splesh_screen4 } from '../assets';

gsap.registerPlugin(TextPlugin);

const SplashScreen = ({ onProceed }) => {
    useEffect(() => {
        const tl = gsap.timeline();

        tl.to('.text-animation', {
            duration: 0.5,
            opacity: 1,
            y: 0,
            scale: 1,
            ease: "power1.out"
        }).to('.text-animation', {
            duration: 1,
            text: "Biology",
            ease: "power1.out"
        }).to('.text-animation3', {
            duration: 2,
            text: "Practise Questions",
            ease: "power1.out"
        }).to('.text-animation2', {
            duration: 4,
            text: "Practise at your own pace and get evaluated by AI.",
            ease: "power1.out"
        })
            .from('.btn-animation', {
                duration: 1,
                opacity: 0,
                y: 300,
                scale: 0.5,
                ease: "ease.out"
            })
            .to('.btn-animation', {
                duration: 1,
                opacity: 1,
                y: 0,
                scale: 1,
                ease: "ease.in"
            }, "-=0.5");

        // document.body.style.overflow = 'hidden';
    }, []);

    return (
        <div className='relative w-full h-screen'>
            <img className="w-full h-full object-cover" src={splesh_screen4} alt="" />
            <div className="splash-screen w-full h-screen flex flex-col items-center mt-[40%] sm:mt-[30%] md:mt-[21%] lg:mt-[15%] lg:ml-[20%] xl:mt-[8%] text-center font-bold absolute z-10 top-0 font-serif">
                <h1 className='text-[50px] sm:text-[80px] font-bold p-1 md:p-0 text-animation'></h1>
                <h1 className='text-4xl p-1 md:p-0 text-animation3'></h1>
                <h2 className='text-2xl p-5 md:p-0 text-animation2'></h2>
                <button className="p-3 px-8 sm:px-10 md:px-14 rounded-full btn-animation md:mt-4 bg-black/90 text-white/90" onClick={onProceed} >Proceed to Practice</button>
            </div>
        </div>
    );
};

export default SplashScreen;
