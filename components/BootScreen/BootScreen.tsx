import React, { useEffect, useState } from 'react';
import styles from './BootScreen.module.css';

interface BootScreenProps {
  onBootComplete: () => void;
}

interface BootScreenSettings {
  boot_screen_line1: string;
  boot_screen_line2: string;
  boot_screen_copyright: string;
}

const BootScreen: React.FC<BootScreenProps> = ({ onBootComplete }) => {
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [bootSettings, setBootSettings] = useState<BootScreenSettings>({
    boot_screen_line1: "Sujay's",
    boot_screen_line2: "Portfolio",
    boot_screen_copyright: "Copyright © Sujay K"
  });

  useEffect(() => {
    fetch('/api/site-settings')
      .then(response => response.json())
      .then(data => {
        if (data.boot_screen_line1 || data.boot_screen_line2 || data.boot_screen_copyright) {
          setBootSettings({
            boot_screen_line1: data.boot_screen_line1 || "Sujay's",
            boot_screen_line2: data.boot_screen_line2 || "Portfolio",
            boot_screen_copyright: data.boot_screen_copyright || "Copyright © Sujay K"
          });
        }
      })
      .catch(error => {
        console.error('Failed to fetch boot screen settings:', error);
      });

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
            <span className={styles.sujay}>{bootSettings.boot_screen_line1}</span>
            <span className={styles.portfolio}>{bootSettings.boot_screen_line2}</span>
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
          {bootSettings.boot_screen_copyright}
        </div>
      </div>
    </div>
  );
};

export default BootScreen;
