import axios from 'axios';
axios.defaults.baseURL = '/api/v1';

export const loginUser = async ({username,password})=> {
	return await axios.post('/auth/login',{username, password}).then(res=>res.data);
};

export const indentifyUser = async ()=> {
	return await axios.get('/auth/identify').then(res=>res.data);
};
export const logoutUser = async ()=> {
	return await axios.delete('/auth/logout').then(res=>res.data);
};
export const fetchAsset= async (id)=> {
	return await axios.get(`/asset/get/${id}`).then(res=>res.data);
};
