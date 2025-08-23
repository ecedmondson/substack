import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from '~/shared/pages/Home';
import PageLayout from '~/shared/components/PageLayout';
import MessageViewerPage from '~/shared/pages/MessageViewer';
import RelayViewerPage from '~/shared/pages/RelayViewer';
import ContactViewerPage from '~/shared/pages/Contact';

const AppRoutes = () => (
  <Routes>
    <Route element={<PageLayout />} >
      <Route path="/" element={<Home />} />
      <Route path="/messages" element={<MessageViewerPage />} />
      <Route path="/relay" element={<RelayViewerPage />} />
      <Route path="/contacts" element={<ContactViewerPage />} />
    </Route>
  </Routes>
);

export default AppRoutes;
