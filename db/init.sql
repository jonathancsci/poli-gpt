-- Create the 'liberal' table
CREATE TABLE liberal (
    id SERIAL PRIMARY KEY,
    headline VARCHAR(255),
    body TEXT,
    url VARCHAR(255)
);

-- Insert sample articles into the 'liberal' table
INSERT INTO liberal (headline, body, url) VALUES
('Liberal Headline 1', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor.', 'http://example.com/liberal1'),
('Liberal Headline 2', 'Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie.', 'http://example.com/liberal2'),
('Liberal Headline 3', 'Phasellus ultrices nulla quis nibh. Quisque a lectus. Donec consectetuer ligula vulputate sem tristique cursus. Nam nulla quam, gravida non, commodo a, sodales sit amet, nisi.', 'http://example.com/liberal3');

-- Create the 'conservative' table
CREATE TABLE conservative (
    id SERIAL PRIMARY KEY,
    headline VARCHAR(255),
    body TEXT,
    url VARCHAR(255)
);

-- Insert sample articles into the 'conservative' table
INSERT INTO conservative (headline, body, url) VALUES
('Conservative Headline 1', 'Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante.', 'http://example.com/conservative1'),
('Conservative Headline 2', 'Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo. Quisque sit amet est et sapien ullamcorper pharetra.', 'http://example.com/conservative2'),
('Conservative Headline 3', 'Vestibulum erat wisi, condimentum sed, commodo vitae, ornare sit amet, wisi. Aenean fermentum, elit eget tincidunt condimentum, eros ipsum rutrum orci, sagittis tempus lacus enim ac dui.', 'http://example.com/conservative3');
