import { useEffect } from "react";
import Image from "next/image";
import styles from "./ImageViewer.module.css";

interface DesignItem {
  id: number;
  title: string;
  description?: string;
  file_url: string;
  thumbnail_url?: string;
  file_type?: string;
  client_name?: string;
  project_date?: string;
  tags?: string;
  width?: number;
  height?: number;
}

interface Props {
  item: DesignItem;
  onClose: () => void;
}

const ImageViewer = ({ item, onClose }: Props) => {
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose();
      }
    };
    window.addEventListener("keydown", handleEsc);
    return () => window.removeEventListener("keydown", handleEsc);
  }, [onClose]);

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.window} onClick={(e) => e.stopPropagation()}>
        <div className={styles.titleBar}>
          <div className={styles.titleBarText}>
            <span>{item.title}</span>
          </div>
          <button className={styles.closeButton} onClick={onClose}>
            <span>×</span>
          </button>
        </div>

        <div className={styles.toolbar}>
          <div className={styles.toolbarButtons}>
            <button className={styles.toolButton}>File</button>
            <button className={styles.toolButton}>Edit</button>
            <button className={styles.toolButton}>View</button>
          </div>
        </div>

        <div className={styles.content}>
          <div className={styles.imageContainer}>
            <img
              src={item.file_url}
              alt={item.title}
              className={styles.image}
            />
          </div>

          <div className={styles.infoPanel}>
            <div className={styles.infoSection}>
              <h4>Details</h4>
              {item.description && <p><strong>Description:</strong> {item.description}</p>}
              {item.client_name && <p><strong>Client:</strong> {item.client_name}</p>}
              {item.project_date && <p><strong>Date:</strong> {new Date(item.project_date).toLocaleDateString()}</p>}
              {item.tags && <p><strong>Tags:</strong> {item.tags}</p>}
              {item.width && item.height && (
                <p><strong>Dimensions:</strong> {item.width} × {item.height}</p>
              )}
            </div>
          </div>
        </div>

        <div className={styles.statusBar}>
          <span className={styles.statusText}>Ready</span>
        </div>
      </div>
    </div>
  );
};

export default ImageViewer;
