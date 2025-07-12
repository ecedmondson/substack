import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from '~/shared/pages/Home';
import Layout from '~/shared/components/Layout';

const AppRoutes = () => (
  <Routes>
    <Route element={<Layout />} >
      <Route path="*" element={<Home />} />
    </Route>
  </Routes>
);

export default AppRoutes;
