// src/App.js
import React, { useEffect, useState } from "react";
import { useMsal } from "@azure/msal-react";
import { loginRequest } from "./authConfig";
import UserTable from "./UserTable";
import { Container, Button, Typography } from "@mui/material";

function App() {
  const { instance, accounts } = useMsal();
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    const initializeMsal = async () => {
      try {
        console.log("Initializing MSAL...");
        const response = await instance.handleRedirectPromise();
        if (response) {
          console.log("Response received:", response);
          instance.setActiveAccount(response.account);
        }
        // 認可コードを処理した後にURLをクリーンアップ
        window.history.replaceState(
          {},
          document.title,
          window.location.pathname
        );
      } catch (e) {
        console.error("Error during MSAL initialization:", e);
      } finally {
        setIsInitialized(true); // MSAL の初期化が完了したらフラグを設定
        console.log("MSAL initialization complete");
      }
    };

    initializeMsal();
  }, [instance]);

  const handleLogin = () => {
    console.log("Starting login process...");
    instance.loginRedirect(loginRequest);
  };

  const handleLogout = () => {
    console.log("Starting logout process...");
    instance.logoutRedirect();
  };

  if (!isInitialized) {
    return <div>Loading...</div>; // 初期化が完了するまでローディング画面を表示
  }

  return (
    <Container>
      <Typography variant="h4" component="h1" gutterBottom>
        Welcome to the User Info App
      </Typography>
      {accounts.length === 0 ? (
        <Button variant="contained" color="primary" onClick={handleLogin}>
          Login
        </Button>
      ) : (
        <div>
          <Button variant="contained" color="secondary" onClick={handleLogout}>
            Logout
          </Button>
          <UserTable />
        </div>
      )}
    </Container>
  );
}

export default App;
