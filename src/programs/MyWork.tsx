import { useEffect, useState } from "react";
import styles from "./MyWork.module.css";
import FolderView from "components/FolderView/FolderView";
import ImageViewer from "components/ImageViewer/ImageViewer";
import axios from "axios";

interface Props {
  id: number;
}

interface Folder {
  id: number;
  name: string;
  description?: string;
  icon_type: string;
  item_count: number;
}

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

const MyWork = ({ id }: Props) => {
  const [folders, setFolders] = useState<Folder[]>([]);
  const [currentFolderId, setCurrentFolderId] = useState<number | null>(null);
  const [currentFolderItems, setCurrentFolderItems] = useState<DesignItem[]>([]);
  const [currentFolderName, setCurrentFolderName] = useState<string>("");
  const [selectedItem, setSelectedItem] = useState<DesignItem | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFolders();
  }, []);

  const fetchFolders = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/api/folders");
      setFolders(response.data);
    } catch (error) {
      console.error("Error fetching folders:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleFolderClick = async (folderId: number) => {
    try {
      setLoading(true);
      const folderResponse = await axios.get(`/api/folders/${folderId}`);
      const itemsResponse = await axios.get(`/api/folders/${folderId}/work`);
      
      setCurrentFolderId(folderId);
      setCurrentFolderName(folderResponse.data.name);
      setCurrentFolderItems(itemsResponse.data);
    } catch (error) {
      console.error("Error fetching folder items:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleBackClick = () => {
    setCurrentFolderId(null);
    setCurrentFolderItems([]);
    setCurrentFolderName("");
  };

  const handleItemClick = (item: DesignItem) => {
    setSelectedItem(item);
  };

  const handleCloseViewer = () => {
    setSelectedItem(null);
  };

  return (
    <div className={styles.main}>
      <div className={styles.explorerPane}>
        <div className={styles.taskPanel}>
          <div className={styles.taskSection}>
            <h3 className={styles.taskTitle}>Design Portfolio</h3>
            <p className={styles.taskDescription}>
              Welcome to my design portfolio! Browse through my work organized in folders.
            </p>
          </div>
          
          <div className={styles.taskSection}>
            <h3 className={styles.taskTitle}>Folder Tasks</h3>
            <ul className={styles.taskList}>
              <li className={styles.taskItem}>
                Double-click a folder to open it
              </li>
              <li className={styles.taskItem}>
                Click on an image to view details
              </li>
              <li className={styles.taskItem}>
                Use the Back button to return
              </li>
            </ul>
          </div>

          {currentFolderId && (
            <div className={styles.taskSection}>
              <h3 className={styles.taskTitle}>Other Places</h3>
              <ul className={styles.taskList}>
                <li className={styles.taskLink} onClick={handleBackClick}>
                  ← My Design Work
                </li>
              </ul>
            </div>
          )}
        </div>
      </div>

      <div className={styles.contentPane}>
        {loading ? (
          <div className={styles.loading}>Loading...</div>
        ) : (
          <FolderView
            folders={folders}
            onFolderClick={handleFolderClick}
            currentFolderItems={currentFolderId ? currentFolderItems : undefined}
            currentFolderName={currentFolderName}
            onBackClick={handleBackClick}
            onItemClick={handleItemClick}
          />
        )}
      </div>

      {selectedItem && (
        <ImageViewer item={selectedItem} onClose={handleCloseViewer} />
      )}
    </div>
  );
};

export default MyWork;
