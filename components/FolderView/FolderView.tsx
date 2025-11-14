import { useState } from "react";
import Image from "next/image";
import styles from "./FolderView.module.css";
import folderIcon from "../../assets/folder.png";

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
}

interface Folder {
  id: number;
  name: string;
  description?: string;
  icon_type: string;
  item_count: number;
}

interface Props {
  folders: Folder[];
  onFolderClick: (folderId: number) => void;
  onItemClick?: (item: DesignItem) => void;
  currentFolderItems?: DesignItem[];
  currentFolderName?: string;
  onBackClick?: () => void;
}

const FolderView = ({
  folders,
  onFolderClick,
  onItemClick,
  currentFolderItems,
  currentFolderName,
  onBackClick,
}: Props) => {
  const isInFolderView = currentFolderItems !== undefined;

  return (
    <div className={styles.container}>
      {isInFolderView && (
        <div className={styles.header}>
          <button onClick={onBackClick} className={styles.backButton}>
            ← Back
          </button>
          <h3 className={styles.folderTitle}>{currentFolderName}</h3>
        </div>
      )}

      <div className={styles.folderGrid}>
        {!isInFolderView ? (
          folders.map((folder) => (
            <div
              key={folder.id}
              className={styles.folderItem}
              onClick={() => onFolderClick(folder.id)}
              onDoubleClick={() => onFolderClick(folder.id)}
            >
              <div className={styles.iconWrapper}>
                <Image
                  src={folderIcon}
                  alt="Folder"
                  width={48}
                  height={48}
                  className={styles.folderIconImg}
                />
              </div>
              <div className={styles.label}>
                <span>{folder.name}</span>
                {folder.item_count > 0 && (
                  <span className={styles.itemCount}>
                    ({folder.item_count} items)
                  </span>
                )}
              </div>
            </div>
          ))
        ) : (
          currentFolderItems.map((item) => (
            <div
              key={item.id}
              className={styles.fileItem}
              onClick={() => onItemClick?.(item)}
              onDoubleClick={() => onItemClick?.(item)}
            >
              <div className={styles.thumbnailWrapper}>
                {item.thumbnail_url ? (
                  <img
                    src={item.thumbnail_url}
                    alt={item.title}
                    className={styles.thumbnail}
                  />
                ) : (
                  <div className={styles.noThumbnail}>
                    <Image
                      src={require("../../assets/image.png")}
                      alt="File"
                      width={48}
                      height={48}
                    />
                  </div>
                )}
              </div>
              <div className={styles.fileLabel}>
                <span>{item.title}</span>
              </div>
            </div>
          ))
        )}
      </div>

      {!isInFolderView && folders.length === 0 && (
        <div className={styles.emptyState}>
          <p>No folders yet. Use the admin panel to create folders and add your design work.</p>
        </div>
      )}

      {isInFolderView && currentFolderItems.length === 0 && (
        <div className={styles.emptyState}>
          <p>This folder is empty.</p>
        </div>
      )}
    </div>
  );
};

export default FolderView;
