import React, { useEffect, useState } from 'react';
import styles from './BootScreen.module.css';

interface BootScreenProps {
  onBootComplete: () => void;
}

const BootScreen: React.FC<BootScreenProps> = ({ onBootComplete }) => {
  const [loadingProgress, setLoadingProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setLoadingProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 8;
      });
    }, 240);

    const timer = setTimeout(() => {
      onBootComplete();
    }, 3000);

    return () => {
      clearInterval(interval);
      clearTimeout(timer);
    };
  }, [onBootComplete]);

  return (
    <div className={styles.bootScreen}>
      <div className={styles.content}>
        <div className={styles.logo}>
          <img src="/images/xp-boot.png" alt="Boot Screen" />
        </div>
        <div className={styles.brandingContainer}>
          <div className={styles.branding}>
            <span className={styles.sujay}>Sujay&apos;s</span>
            <span className={styles.portfolio}>Portfolio</span>
          </div>
        </div>
        <div className={styles.loadingBarContainer}>
          <div className={styles.loadingBar}>
            <div 
              className={styles.loadingProgress}
              style={{ width: `${loadingProgress}%` }}
            />
          </div>
        </div>
        <div className={styles.copyright}>
          Copyright © Sujay K
        </div>
      </div>
    </div>
  );
};

export default BootScreen;
