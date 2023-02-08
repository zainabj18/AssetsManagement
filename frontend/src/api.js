import axios from 'axios';
axios.defaults.baseURL = '/api/v1';

export const loginUser = async ({ username, password }) => {
	return await axios.post('/auth/login', { username, password }).then(res => res.data);
};

export const indentifyUser = async () => {
	return await axios.get('/auth/identify').then(res => res.data);
};
export const logoutUser = async () => {
	return await axios.delete('/auth/logout').then(res => res.data);
};
export const fetchAsset = async (id) => {
	return await axios.get(`/asset/get/${id}`).then(res => res.data);
};
export const fetchAssetClassifications= async ()=> {
	return await axios.get('/asset/classifications').then(res=>res.data);
};

export const fetchTags= async ()=> {
	return await axios.get('/tag/').then(res=>res.data);
};

export const createTag= async (tag)=> {
	return await axios.post('/tag/',{'name':tag}).then(res=>res.data);
};

export const fetchProjects= async ()=> {
	return await axios.get('/project/').then(res=>res.data);
};

export const fetchAllTypes = async () => {
	return await axios.get('/type/allTypes').then(res => res.data);
};

export const fetchAllAttributes = async () => {
	return await axios.get('/type/allAttributes').then(res => res.data);
};

export const createAttribute = async (newAttribute) => {
	return await axios.post('/type/adder/new', newAttribute).then(res => res.data);
};

export const createType = async (newType) => {
	return await axios.post('/type/new', newType).then(res => res.data);
};