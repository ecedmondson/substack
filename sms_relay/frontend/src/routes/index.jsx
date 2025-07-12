import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from '~/shared/pages/Home';
import Layout from '~/shared/components/Layout';
import MessageViewerPage from '~/shared/pages/MessageViewer';

const AppRoutes = () => (
  <Routes>
    <Route element={<Layout />} >
      <Route path="*" element={<Home />} />
      <Route path="/messages" element={<MessageViewerPage />} />
    </Route>
  </Routes>
);

export default AppRoutes;
