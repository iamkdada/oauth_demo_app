// src/UserTable.js
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useMsal } from "@azure/msal-react";
import { InteractionRequiredAuthError } from "@azure/msal-browser";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Container,
  Typography,
} from "@mui/material";

function UserTable() {
  const { instance, accounts } = useMsal();
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      if (accounts.length > 0) {
        const accessTokenRequest = {
          scopes: ["<application id uri>/User.Read"],
          account: accounts[0],
        };

        try {
          const tokenResponse = await instance.acquireTokenSilent(
            accessTokenRequest
          );
          const headers = {
            Authorization: `Bearer ${tokenResponse.accessToken}`,
          };

          const response = await axios.get("http://localhost:8000/users/", {
            headers,
          });
          setUsers(response.data);
        } catch (e) {
          if (e instanceof InteractionRequiredAuthError) {
            instance.acquireTokenRedirect(accessTokenRequest);
          } else {
            console.error(e);
          }
        }
      }
    };

    fetchData();
  }, [accounts, instance]);

  return (
    <Container>
      <Typography variant="h5" component="h2" gutterBottom>
        User Information
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Email</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.id}</TableCell>
                <TableCell>{user.name}</TableCell>
                <TableCell>{user.email}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
}

export default UserTable;
