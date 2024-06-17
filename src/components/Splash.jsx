import React, { useState, useEffect, useRef } from 'react';
import gsap from 'gsap';
import { TextPlugin } from 'gsap/TextPlugin';
import SplashScreen from './SplashScreen';
import MainContent from './MainContent';

gsap.registerPlugin(TextPlugin);

const Splash = () => {
    const [loading, setLoading] = useState(true);
    const mainContentRef = useRef(null);
    const splashScreenRef = useRef(null);

    const handleProceed = () => {
        const tl = gsap.timeline({
            onComplete: () => setLoading(false)
        });

        tl.to(splashScreenRef.current, {
            x: '-100%',
            ease: 'power1.inOut'
        })
            .set(mainContentRef.current, { x: '100%', opacity: 1, display: 'block' })
            .to(mainContentRef.current, {
                duration: 0.5,
                x: '0',
                ease: 'power1.inOut'
            });
    };

    useEffect(() => {
        if (!loading) {
            gsap.set(mainContentRef.current, { display: 'block', x: '0', opacity: 1 });
        }
    }, [loading]);

    return (
        <div className="relative w-full h-full overflow-hidden">
            <div ref={splashScreenRef} className="splash-screen w-full h-full fixed top-0 left-0">
                {loading && <SplashScreen onProceed={handleProceed} />}
            </div>
            <div
                className={`bg-white w-full h-full fixed top-0 left-0 flex justify-center items-center overflow-y-scroll`}
                ref={mainContentRef}
                style={{ opacity: loading ? 0 : 1, display: 'none' }}
            >
                <MainContent />
            </div>
        </div>
    );
};

export default Splash;
