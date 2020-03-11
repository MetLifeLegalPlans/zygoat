import axios from 'axios';

const fetcher = async (req, res) => {
  const {
    query: { slug, ...params },
    headers,
    body: data,
  } = req;

  const config = { params, headers, validateStatus: () => true };
  const url = `${process.env.BACKEND_URL}/api/${slug.join('/')}/`;

  let response = null;

  if (req.method === 'GET') {
    response = await axios.get(url, config);
  } else {
    response = await axios[req.method.toLowerCase()](url, data, config);
  }

  const setHeader = ([name, value]) => res.setHeader(name, value)
  Object.entries(response.headers).forEach(setHeader);

  res.status(response.status);
  res.json(response.data);
  res.end();
};

export default fetcher;
